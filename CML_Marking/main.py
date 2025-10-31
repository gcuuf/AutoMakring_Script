from pathlib import Path
import pandas as pd
import re
import os
from config import HTML_FILEPATH
import utils
from network_connector import connect
from report_generator import initialize_html, add_card_to_html, complete_html, save_and_open_report, score_summary

def check_configuration(check_name, commands, expected_values, nodes, note=None, score=0, id=None):
    node_results = []
    all_passed = True  # initially set to True, assuming all_pass

    for node in nodes:
        try:
            result_text = ""
            connected = True
            # support multiple commands execution
            for cmd in commands:
                cmd_connected, cmd_output = connect(node, cmd)
                if not cmd_connected:
                    connected = False
                    result_text = cmd_output
                    break
                result_text += cmd_output + "\n"
        except Exception as e:
            connected = False
            result_text = f"Connection error: {str(e)}"

        if connected:
            # === Expected values check ===
            found_values = []
            missing_values = []
            for ev in expected_values:
                pattern = rf'(?<!\S){re.escape(ev)}(?!\S)'
                if re.search(pattern, result_text, re.IGNORECASE):
                    found_values.append(ev)
                else:
                    missing_values.append(ev)

            passed = len(missing_values) == 0
            if passed:
                found_values_str = ", ".join(found_values) if found_values else "None"
                node_results.append(f"✅ Node {node}: Success (Found: {found_values_str})\n{result_text}")
            else:
                found_values_str = ", ".join(found_values) if found_values else "None"
                missing_values_str = ", ".join(missing_values) if missing_values else "None"
                node_results.append(
                    f"❌ Node {node}: Incorrect configuration (Found: {found_values_str}, Missing: {missing_values_str})\n{result_text}"
                )
                all_passed = False
        else:
            node_results.append(f"❌ Node {node}: Connection failed\n{result_text}")
            all_passed = False

    expected_values_str = ", ".join(expected_values) if expected_values else "None"
    combined_result = f"Expected values: {expected_values_str}\n\n" + "\n\n".join(node_results)
    status_text = f"✅ {check_name} correct" if all_passed else f"❌ {check_name} incorrect"

    utils.add_check_result(
        title=check_name,
        status_text=status_text,
        passed=all_passed,
        score=score,
        raw_output=combined_result,
        note=note,
        id=id
    )


def main():
    utils.global_total_score = 0  # reset total score
    print("Starting network device configuration check...")

    # read Excel configuration
    excel_path = os.path.join(os.path.dirname(__file__), 'check_configuration.xlsx')
    try:
        df = pd.read_excel(excel_path)
        df = df.dropna(subset=['check_name']).drop_duplicates(subset=['check_name'], keep='first')
        df['check_name'] = df['check_name'].str.strip().str.lower()
    except FileNotFoundError:
        print(f"Error: Configuration file {excel_path} not found")
        return
    except Exception as e:
        print(f"Read configuration file failed: {str(e)}")
        return

    processed_checks = set()
    for _, row in df.iterrows():
        check_name = row['check_name'].lower()
        if check_name in processed_checks:
            continue
        processed_checks.add(check_name)
        check_configuration(
            check_name=row['check_name'],
            commands=[cmd.strip() for cmd in str(row['command']).split(',')] if pd.notna(row['command']) else [],
            expected_values=[ev.strip() for ev in str(row['expected_values']).split(',') if ev.strip()] if pd.notna(row['expected_values']) else [],    
            nodes=[node.strip() for node in str(row['node']).split(',')] if pd.notna(row['node']) else [],
            note=row['note'] if pd.notna(row['note']) else None,
            score=float(row['score']) if pd.notna(row['score']) else 0,
            id=row['id'] if pd.notna(row['id']) else None
        )

    # generate HTML report
    print("\nGenerating HTML report...")
    html = initialize_html()
    # 按ID排序结果并分组编号
    sorted_results = sorted(utils.global_results, key=lambda x: x.id)
    id_counter = {}
    for result in sorted_results:
        result_id = result.id or "unknown"
        id_counter[result_id] = id_counter.get(result_id, 0) + 1
        current_index = id_counter[result_id]
        note = getattr(result, 'note', None)
        html = add_card_to_html(html, result, current_index, note=note)
    html = complete_html(html, utils)
    save_and_open_report(html)
    print("\nCheck completed! Report has been opened automatically.")


if __name__ == "__main__":
    main()

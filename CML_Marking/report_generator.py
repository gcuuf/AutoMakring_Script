import os
import webbrowser
from datetime import datetime
from config import HTML_OUTPUT_DIR, HTML_FILEPATH
import utils

def initialize_html():
    return f'''
<html>
<head>
<meta charset='UTF-8'>
<title>Scoring Result Check Report</title>
<style>
body {{
    font-family: "Segoe UI", Arial, sans-serif;
    background: linear-gradient(135deg, #0f172a, #1e293b);
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 30px;
  }}
h1 {{
    color: white;
    text-align: center;
}}
.card {{
    width: 60%;
    background: white;
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    margin: 15px;
    padding: 20px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}}
.card:hover {{
    transform: scale(1.02);
    box-shadow: 0 8px 20px rgba(0,0,0,0.2);
}}
.ok {{ border: 3px solid #4CAF50; }}
.fail {{ border: 3px solid #f44336; }}
.note {{
    border: 3px solid #FFC107; /* 黄色边框 */
    font-weight: bold;
    color: #800080; /* 紫色 */
    margin-top: 1em;
    margin-bottom: 1em;
}}
.question-title {{
    font-size: 18px;
    color: #0078d7;
    font-weight: bold;
}}
.status {{
    font-size: 16px;
    margin-top: 8px;
}}
.score {{
    font-size: 14px;
    color: #333;
    margin-top: 6px;
}}
.raw-output {{
    font-family: Consolas, monospace;
    background-color: #f1f1f1;
    padding: 10px;
    margin-top: 10px;
    border-radius: 8px;
    white-space: pre-wrap;
    font-size: 13px;
    color: #333;
    max-height: 400px;
    overflow-y: auto;
    border-left: 4px solid #ccc;
}}
.final {{
    width: 65%;
    text-align: center;
    font-size: 22px;
    font-weight: bold;
    padding: 25px;
    border-radius: 20px;
    background-color: #fff;
    box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    margin-top: 40px;
}}
button {{
    margin-top: 10px;
    padding: 6px 12px;
    font-size: 13px;
    border-radius: 8px;
    border: none;
    cursor: pointer;
    transition: 0.2s;
}}
button.correct {{
    background-color: #4CAF50;
    color: white;
}}
button.wrong {{
    background-color: #f44336;
    color: white;
    margin-left: 8px;
}}
button:hover {{ opacity: 0.8; }}
</style>
</head>
<body>
<h1 style='color: white;'>Scoring Result Check Report - {datetime.now().strftime('%Y/%m/%d %H:%M:%S')}</h1>

<script>
function updateScore() {{
    var total = 0;
    var max = 0;
    document.querySelectorAll('.card').forEach(function(card){{
        var score = parseFloat(card.getAttribute('data-score'));
        var passed = card.classList.contains('ok');
        max = Math.round((max + score) * 100) / 100;
        if (passed) total = Math.round((total + score) * 100) / 100;
    }});
    document.getElementById('final-score').innerText = 'Final Score: ' + total.toFixed(2) + ' / Total Points: ' + max.toFixed(2);
}}

function markCard(el, passed) {{
    var card = el.closest('.card');
    card.classList.remove('ok', 'fail', 'note');
    var status = card.querySelector('.status b');
    if (passed) {{
        card.classList.add('ok');
        status.innerText = '✅ Confirmed Correct';
        status.style.color = '#4CAF50';
    }} else {{
        card.classList.add('fail');
        status.innerText = '❌ Confirmed Incorrect';
        status.style.color = '#f44336';
    }}
    updateScore();
}}
</script>
'''

def add_card_to_html(html, result, index, note=None):
    # 修改边框类和状态颜色逻辑，当有note时设置为黄色
    if note:
        border_class = "note"
        status_color = "#FFC107"  # 黄色
    else:
        border_class = "ok" if result.passed else "fail"
        status_color = "#4CAF50" if result.passed else "#f44336"
    
    earned = result.score if result.passed else 0
    
    raw_section = ""
    if result.raw_output:
        raw_section = f"\n    <div class='raw-output'><pre>{result.raw_output}</pre></div>"

    note_section = f"\n    <div class='note'>Note: {note}</div>" if note else ""

    card_html = f'''
<div class='card {border_class}' data-score='{result.score:.2f}'>
    <div class='question-title'>{index}. {result.title}</div>
    {note_section}
    <div class='status'><b style='color:{status_color};'>{result.status_text}</b></div>
    <div class='score'>Score: {earned} / Points: {result.score}</div>
    <div>
        <button class='correct' onclick='markCard(this, true)'>Confirm Correct ✅</button>
        <button class='wrong' onclick='markCard(this, false)'>Confirm Incorrect ❌</button>
    </div>{raw_section}
</div>
'''
    return html + card_html

from utils import global_total_score, global_max_score

def complete_html(html):
    return html + f'''
<div class='final' id='final-score'>
Final Score: {utils.global_total_score:.2f} / Total Points: {utils.global_max_score:.2f}
</div>
</body></html>
'''

def save_and_open_report(html_content):
    if not os.path.exists(HTML_OUTPUT_DIR):
        os.makedirs(HTML_OUTPUT_DIR)
    
    with open(HTML_FILEPATH, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Report generated: {HTML_FILEPATH}")
    webbrowser.open(HTML_FILEPATH)

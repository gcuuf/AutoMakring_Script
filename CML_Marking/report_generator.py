import os
import webbrowser
from datetime import datetime
from config import HTML_OUTPUT_DIR, HTML_FILEPATH
import utils
score_summary = []

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
.score-summary {{
    width: 80%;
    border-collapse: collapse;
    margin: 20px 0;
    color: white;
}}
.score-summary th, .score-summary td {{
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
}}
.score-summary th {{
    background-color: #334155;
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
.card-with-note {{
    border: 3px solid #FFC107; /* 黄色边框 */
}}
.note {{
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
    padding: 8px 16px; /* 增加按钮的填充，使其更显眼 */
    font-size: 14px; /* 稍微增加字体大小 */
    border-radius: 12px; /* 增加圆角，使按钮看起来更现代 */
    border: 1px solid transparent; /* 使用透明边框来避免闪烁的边界 */
    cursor: pointer;
    transition: all 0.3s ease; /* 使所有的过渡效果更加平滑 */
    background-color: #3498db; /* 默认背景色为蓝色 */
    color: #fff; /* 默认文本颜色为白色 */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* 添加阴影，增加立体感 */
}}

button.correct.active {{
    background-color: #4CAF50; /* 绿色按钮 */
    color: white;
    box-shadow: 0 6px 12px rgba(0, 255, 0, 0.3); /* 更强烈的绿色阴影，增加活力感 */
    transform: scale(1.05); /* 在激活时稍微放大按钮，给人一种按钮被按下的感觉 */
}}

button.wrong {{     
    margin-left: 12px; /* 增加左边距，使按钮之间的间隔更均匀 */
    color: #4B0082; /* 默认文本颜色为紫色 */
    background-color: #FFC107; /* 默认背景色为黄色 */
}}

button.wrong.active {{
    background-color: #f44336; /* 深红色按钮 */
    color: white;
    box-shadow: 0 6px 12px rgba(255, 0, 0, 0.3); /* 红色的阴影，更加显眼 */
    transform: scale(1.05); /* 激活时按钮轻微放大 */
}}

button:hover {{
    opacity: 0.9; /* 悬停时稍微改变透明度 */
    transform: translateY(-2px); /* 悬停时轻微向上移动，增加互动感 */
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3); /* 增强悬停时的阴影效果 */
}}

button:active {{
    transform: scale(0.98); /* 按下按钮时稍微缩小 */
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2); /* 按下时减少阴影 */
}}
</style>
</head>
<script>
function updateScore() {{
    var total = 0;
    var max = 0;
    document.querySelectorAll('.card').forEach(function(card) {{
        var score = parseFloat(card.getAttribute('data-score'));
        var passed = card.classList.contains('ok');
        max = Math.round((max + score) * 100) / 100;
        if (passed) total = Math.round((total + score) * 100) / 100;

        // 获取卡片索引（从标题中提取）
        var titleElement = card.querySelector('.question-title');
        var index = titleElement.textContent.split('.')[0];

        // 更新汇总表中的Earned分值
        var earnedCell = document.getElementById('earned-' + index);
        if (earnedCell) {{
            earnedCell.textContent = passed ? score : '0';
        }}
    }});
    document.getElementById('final-score').innerText = 'Final Score: ' + total.toFixed(2) + ' / Total Points: ' + max.toFixed(2);
}}


function markCard(el, passed) {{
    var card = el.closest('.card');
    card.classList.remove('ok', 'fail', 'card-with-note');
    // 移除所有按钮的active类
    card.querySelectorAll('button').forEach(btn => btn.classList.remove('active'));
    // 为当前点击的按钮添加active类
    el.classList.add('active');
    var status = card.querySelector('.status b');
    var scoreElement = card.querySelector('.score');
    var maxScore = card.dataset.score;
    if (passed) {{
        card.classList.add('ok');
        status.innerText = '✅ Confirmed Correct';
        status.style.color = '#4CAF50';
        scoreElement.textContent = 'Score: ' + maxScore + ' / Points: ' + maxScore;
    }} else {{
        card.classList.add('fail');
        status.innerText = '❌ Confirmed Incorrect';
        status.style.color = '#f44336';
        scoreElement.textContent = 'Score: 0 / Points: ' + maxScore;
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
<div class='card {border_class} {"card-with-note" if note else ""}' data-score='{result.score:.2f}'>
    <div class='question-title'>{index}. {result.title}</div>
    {note_section}
    <div class='status'><b style='color:{status_color};'>{result.status_text}</b></div>
    <div class='score'>Score: {earned} / Points: {result.score}</div>
    <div>
        <button class='correct' onclick='markCard(this, true)'>CONFIRM CORRECT</button>
        <button class='wrong' onclick='markCard(this, false)'>CONFIRM INCORRECT</button>
    </div>{raw_section}
</div>
'''
    # 添加分数数据到汇总列表
    score_summary.append({
        'index': index,
        'title': result.title,
        'earned': earned,
        'score': result.score
    })
    return html + card_html

from utils import global_total_score, global_max_score

def complete_html(html):
    table_html = "<table class='score-summary'><tr><th>Index</th><th>Aspect - Description</th><th>Earned</th><th>Max Mark</th></tr>"
    for item in score_summary:
        # 为每一行和Earned单元格添加唯一ID
        table_html += f"<tr id='summary-row-{item['index']}'><td>{item['index']}</td><td>{item['title']}</td><td id='earned-{item['index']}'>{item['earned']}</td><td>{item['score']}</td></tr>"
    table_html += "</table>"
    return html + f'''
<div class='final' id='final-score'>
Final Score: {utils.global_total_score:.2f} / Total Points: {utils.global_max_score:.2f}
</div>
{table_html}
</body></html>
'''

def save_and_open_report(html_content):
    if not os.path.exists(HTML_OUTPUT_DIR):
        os.makedirs(HTML_OUTPUT_DIR)
    
    with open(HTML_FILEPATH, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Report generated: {HTML_FILEPATH}")
    webbrowser.open(HTML_FILEPATH)

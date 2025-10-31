import os
import webbrowser
import itertools
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

<script src="xlsx.full.min.js"></script>
<style>
body {{
    font-family: "Segoe UI", Arial, sans-serif;
    background: linear-gradient(135deg, #0f172a, #1e293b);
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 30px;
}}
/* ============ 外层导航栏 ============ */
#sticky-header {{
  position: sticky;
  top: 0;
  left: 0;
  right: 0;
  width: 100vw; /* ✅ 确保铺满整个视口宽度 */
  z-index: 100;
  background: transparent; /* 初始透明 */
  transition: background 0.3s ease, backdrop-filter 0.3s ease, box-shadow 0.3s ease;
}}
/* 滚动后添加视觉强调 */
#sticky-header.scrolled {{
  background: rgba(30, 41, 59, 0.8); /* 半透明深色背景 */
  backdrop-filter: blur(10px);       /* 模糊效果 */
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}}
/* ============ 文本样式 ============ */
.header-container {{
   display: flex;
   align-items: center;
   gap: 16px;
   padding: 8px 0;
 }}
 .header-container label {{
   color: #f1f5f9;
   font-size: 15px;
   font-weight: 600;
   letter-spacing: 0.3px;
   white-space: nowrap;
 }}

.score-summary {{
    width: 80%;
    border-collapse: collapse;
    margin: 20px auto;
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
.group-header {{
    background-color: #334155;
    font-weight: bold;
    color: white;
    text-align: center;
}}
h1 {{
    color: white;
    text-align: center;
}}
.card {{
    width: 100%;
    max-width: 1200px; /* 卡片宽度，可调整 */
    background: rgba(0,0,0,0.3); /* 默认白色背景 */
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    margin: 15px auto;
    padding: 20px;
    transition: all 0.3s ease;
}}
.card.active {{
    background-color: rgba(0,0,0,0.3); /* 黑色背景，透明度30% */
    color: #ffffff; /* 白色文字高亮 */
    box-shadow: 0 6px 18px rgba(0,0,0,0.2);
}}
.card.active .question-title {{
    color: #e0f2fe; /* 标题高亮色 */
}}
.card.active .raw-output {{
    background-color: rgba(30,30,30,0.8); /* 代码块深色背景 */
    color: #ffffff; /* 代码字体白色 */
    border-left-color: #60a5fa;
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
    color: #ffffff;
}}
.raw-output {{
    font-family: Consolas, monospace;
    background-color: rgba(0,0,0,0.3);
    padding: 10px;
    margin-top: 10px;
    border-radius: 8px;
    white-space: pre-wrap;
    font-size: 13px;
    color: #ffffff;
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
    margin: 40px auto 0;
}}
button {{
    margin-top: 10px;
    padding: 8px 16px;
    font-size: 14px;
    border-radius: 12px;
    border: 1px solid transparent;
    cursor: pointer;
    transition: all 0.3s ease;
    background-color: #3498db;
    color: #fff;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}}
button.correct.active {{
    background-color: #4CAF50;
    color: white;
    box-shadow: 0 6px 12px rgba(0, 255, 0, 0.12);
    transform: scale(1.05);
}}
button.wrong {{
    margin-left: 12px;
    color: #4B0082;
    background-color: #FFC107;
}}
button.wrong.active {{
    background-color: #f44336;
    color: white;
    box-shadow: 0 6px 12px rgba(255, 0, 0, 0.12);
    transform: scale(1.05);
}}
button:hover {{
    opacity: 0.9;
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
}}
button:active {{
    transform: scale(0.98);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}}

/* ============ 按钮样式 ============ */
.id-btn {{
  background: linear-gradient(145deg, #475569, #1e293b);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #e2e8f0;
  padding: 6px 14px;
  margin: 4px 8px 4px 0;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.25s ease;
}}

.id-btn:hover {{
  background: linear-gradient(145deg, #64748b, #334155);
  transform: translateY(-1px);
  color: #ffffff;
}}

.id-btn.active {{
  background: linear-gradient(145deg, #0ea5e9, #0284c7);
  color: #fff;
  box-shadow: 0 0 10px rgba(14, 165, 233, 0.3);
  border: none;
}}

.id-btn:active {{
  transform: scale(0.96);
}}

/* 进入动画 */
@keyframes fadeIn {{
  to {{
    opacity: 1;
    transform: scale(1);
  }}
}}
</style>


</head>
<body>

<h1 style='color: white; font-size: 2.5rem; font-weight: bold;'>SCORING RESULT CHECK REPORT - {datetime.now().strftime('%Y/%m/%d %H:%M:%S')}</h1>

<!-- 🔹 全屏铺满的顶部导航栏 -->
<div id="sticky-header">
  <div style="max-width: 1200px; margin: 0 auto;"  class="header-container">
    <label>Select Sub Criteria ID:</label>
    <div id="id-buttons">
      <button class="id-btn active" data-id="all">All IDs</button>
      <!-- 可以在这里动态添加更多按钮 -->
    </div>
  </div>
</div>

  <!-- 内容容器div -->
  <div id='content-container' style='width: 100%;'>

<script>
// 页面滚动时控制导航栏背景变化
window.addEventListener("scroll", function () {{
  const header = document.getElementById("sticky-header");
  if (window.scrollY > 10) {{
    header.classList.add("scrolled");
  }} else {{
    header.classList.remove("scrolled");
  }}
}});

// --- ID 切换功能（已修正） ---
function populateIdSelector() {{
    const buttonContainer = document.getElementById('id-buttons');
    const cards = document.querySelectorAll('.card');
    const ids = new Set();

    cards.forEach(card => {{
        const id = card.getAttribute('data-id') || 'unknown';
        if (id && id !== 'all' && id !== 'unknown') {{
            ids.add(id);
        }}
    }});

    // 移除除第一个（All IDs）外的旧按钮，避免重复生成
    const existing = Array.from(buttonContainer.querySelectorAll('.id-btn'));
    existing.slice(1).forEach(b => b.remove());

    // 按字典序生成按钮（可修改排序逻辑）
    Array.from(ids).sort().forEach(id => {{
        const button = document.createElement('button');
        button.className = 'id-btn';
        button.dataset.id = id;
        const idPrefix = id.split('_')[0];
        button.textContent = idPrefix;
        // 仅使用 class 样式，不直接写入 style 属性（避免覆盖主题）
        button.addEventListener('click', function() {{
            document.querySelectorAll('.id-btn').forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            filterCardsById(this.dataset.id);
        }});
        buttonContainer.appendChild(button);
    }});
}}

// 根据选择的ID筛选卡片
function filterCardsById(id) {{
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {{
        const cardId = card.getAttribute('data-id') || 'unknown';
        const cardPrefix = cardId.split('_')[0];
        if (id === 'all' || cardPrefix === id) {{
            card.classList.add('active');
            card.style.display = 'block';
        }} else {{
            card.classList.remove('active');
            card.style.display = 'none';
        }}
    }});

    // --- 根据ID筛选表格行 ---
    document.querySelectorAll('.score-summary tr').forEach(row => {{
        if (row.classList.contains('group-header')) {{
            const rowId = row.textContent.replace('ID: ','').trim();
            row.style.display = (id === 'all' || rowId === id) ? '' : 'none';
        }} else if (row.id.startsWith('summary-row-')) {{
            const idCell = row.children[1];
            if (idCell) {{
                const rowId = idCell.textContent.split('_')[0];
                row.style.display = (id === 'all' || rowId === id) ? '' : 'none';
            }}
        }}
    }});

    updateScore(); // 筛选后更新分数
}}


// 初始化 ID 选择器并绑定 All IDs 的点击事件
document.addEventListener('DOMContentLoaded', function() {{
    populateIdSelector();

    const allBtn = document.querySelector('.id-btn[data-id="all"]');
    if (allBtn) {{
        allBtn.addEventListener('click', function() {{
            document.querySelectorAll('.id-btn').forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            filterCardsById('all');
        }});
    }}

    // 允许后续在页面上动态添加卡片后再次调用 populateIdSelector()
}});

// 评分更新和标记逻辑（保持原样，按需可继续调整）
function updateScore() {{
    var total = 0;
    var max = 0;
    document.querySelectorAll('.card').forEach(function(card) {{
        // 只计算可见卡片的分数
        if (card.style.display === 'none') return;
        var score = parseFloat(card.getAttribute('data-score')) || 0;
        var passed = card.classList.contains('ok');
        max = Math.round((max + score) * 100) / 100;
        if (passed) total = Math.round((total + score) * 100) / 100;

        // 获取卡片索引（从标题中提取）
        var titleElement = card.querySelector('.question-title');
        var index = titleElement ? titleElement.textContent.split('.')[0] : '';

        // 更新汇总表中的Earned分值
        var earnedCell = document.getElementById('earned-' + index);
        if (earnedCell) {{
            earnedCell.textContent = passed ? score.toFixed(2) : '0.00';
        }}
    }});
    var finalScoreEl = document.getElementById('final-score');
    if (finalScoreEl) {{
        finalScoreEl.innerText = 'Final Score: ' + total.toFixed(2) + ' / Total Points: ' + max.toFixed(2);
    }}
}}

function markCard(el, passed) {{
    var card = el.closest('.card');
    if (!card) return;
    card.classList.remove('ok', 'fail', 'card-with-note');
    // 移除当前卡片中所有确认按钮的 active 类
    card.querySelectorAll('button').forEach(btn => btn.classList.remove('active'));
    // 为当前点击的按钮添加 active 类
    el.classList.add('active');
    var status = card.querySelector('.status b');
    var scoreElement = card.querySelector('.score');
    var maxScore = parseFloat(card.getAttribute('data-score')) || 0;
    if (passed) {{
        card.classList.add('ok');
        if (status) {{ status.innerText = '✅ Confirmed Correct'; status.style.color = '#4CAF50'; }}
        if (scoreElement) {{ scoreElement.textContent = 'Score: ' + maxScore.toFixed(2) + ' / Points: ' + maxScore.toFixed(2); }}
    }} else {{
        card.classList.add('fail');
        if (status) {{ status.innerText = '❌ Confirmed Incorrect'; status.style.color = '#f44336'; }}
        if (scoreElement) {{ scoreElement.textContent = 'Score: 0.00 / Points: ' + maxScore.toFixed(2); }}
    }}
    updateScore();
}}
</script>
'''

# --- 以下函数保持不变（仅粘贴回原文件） ---
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
<div class='card {border_class} {"card-with-note" if note else ""}' data-score='{result.score:.2f}' data-id='{result.id}'>
    <div class='question-title'>{index}. {result.title}</div>
    {note_section}
    <div class='status'><b style='color:{status_color};'>{result.status_text}</b></div>
    <div class='score'>Score: {earned:.2f} / Points: {result.score:.2f}</div>
    <div>
        <button class='correct' onclick='markCard(this, true)'>CONFIRM CORRECT</button>
        <button class='wrong' onclick='markCard(this, false)'>CONFIRM INCORRECT</button>
    </div>{raw_section}
</div>
'''
    # 添加分数数据到汇总列表
    score_summary.append({
        'index': index,
        'id': result.id,
        'title': result.title,
        'earned': f"{earned:.2f}",
        'score': f"{result.score:.2f}"
    })
    return html + card_html

from utils import global_total_score, global_max_score


def complete_html(html, utils):
    # 按ID排序并分组
    sorted_items = sorted(score_summary, key=lambda x: x['id'])
    grouped_items = itertools.groupby(sorted_items, key=lambda x: x['id'].split('_')[0])

    # 构建表格 HTML
    table_html = """
<button onclick="exportToExcel()"
    style="display: block; margin: 10px auto; padding: 8px 16px; 
           background-color: #4CAF50; color: white; border: none; 
           border-radius: 4px; cursor: pointer;">
    导出评分表
</button>

<table class='score-summary' id='scoreTable'>
<tr>
<th>Index</th><th>ID</th><th>Aspect - Description</th><th>Earned</th><th>Max Mark</th>
</tr>
"""
    for id_prefix, items in grouped_items:
        table_html += f"<tr class='group-header'><td colspan='5'>Sub Criteria ID: {id_prefix}</td></tr>"
        for item in items:
            table_html += f"<tr id='summary-row-{item['index']}'><td>{item['index']}</td><td>{item['id']}</td><td>{item['title']}</td><td id='earned-{item['index']}'>{item['earned']}</td><td>{item['score']}</td></tr>"

    table_html += "</table>"

    # 构建完整 HTML
    full_html = f"""
{html}

<div class='final' id='final-score'>
Final Score: {utils.global_total_score:.2f} / Total Points: {utils.global_max_score:.2f}
</div>

{table_html}

<script>
function exportToExcel() {{
    const table = document.getElementById('scoreTable');
    const wb = XLSX.utils.table_to_book(table);
    const today = new Date();
    const dateString = today.getFullYear() + 
        (today.getMonth()+1).toString().padStart(2,'0') + 
        today.getDate().toString().padStart(2,'0');
    const fileName = `ScoringReport_${{dateString}}.xlsx`;
    XLSX.writeFile(wb, fileName);
}}
</script>

<!-- 返回顶部按钮 -->
<button id="back-to-top" class="back-to-top-btn" title="回到顶部">👍</button>

<style>
/* 返回顶部按钮样式 */
.back-to-top-btn {{
    position: fixed;
    bottom: 30px;
    right: 30px;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background: linear-gradient(145deg, #0ea5e9, #0284c7);
    color: white;
    font-size: 24px;
    font-weight: bold;
    border: none;
    box-shadow: 0 4px 12px rgba(14, 165, 233, 0.4);
    cursor: pointer;
    opacity: 0;
    visibility: hidden;
    transition: opacity 0.3s ease, visibility 0.3s ease, transform 0.3s ease;
    z-index: 1000;
    display: flex;
    align-items: center;
    justify-content: center;
}}
.back-to-top-btn.show {{
    opacity: 1;
    visibility: visible;
    transform: translateY(0);
}}
.back-to-top-btn:hover {{
    background: linear-gradient(145deg, #0284c7, #0369a1);
    transform: translateY(-3px);
    box-shadow: 0 6px 16px rgba(14, 165, 233, 0.6);
}}
.back-to-top-btn:active {{
    transform: scale(0.95);
}}

/* 气泡动画样式 */
.bubble {{
    position: absolute;
    pointer-events: none;
    z-index: 9999;
    animation: bubble-animation 4s ease-out forwards;
}}
@keyframes bubble-animation {{
    0% {{ transform: scale(0); opacity: 1; }}
    100% {{ transform: scale(1.5) translateY(-100px) rotate(30deg); opacity: 0; }}
}}
</style>

<script>
const backToTopBtn = document.getElementById('back-to-top');
window.addEventListener('scroll', () => {{
    if (window.pageYOffset > 300) {{
        backToTopBtn.classList.add('show');
    }} else {{
        backToTopBtn.classList.remove('show');
    }}
}});
backToTopBtn.addEventListener('click', (e) => {{
    window.scrollTo({{top: 0, behavior: 'smooth'}});
    
    // 创建点击气泡效果
    const createBubbles = (count) => {{
        const bubbles = ['❤️', '👍', '✨', '🌟', '🎉'];
        const btnRect = backToTopBtn.getBoundingClientRect();
        const startX = btnRect.left + btnRect.width / 2;
        const startY = btnRect.top + btnRect.height / 2;
        
        for (let i = 0; i < count; i++) {{
            const bubble = document.createElement('span');
            bubble.className = 'bubble';
            bubble.textContent = bubbles[Math.floor(Math.random() * bubbles.length)];
            bubble.style.left = `${{startX}}px`;
            bubble.style.top = `${{startY}}px`;
            bubble.style.fontSize = `${{12 + Math.random() * 16}}px`;
            bubble.style.color = `hsl(${{Math.random() * 360}}, 80%, 60%)`;
            bubble.style.transform = `translate(-50%, -50%) rotate(${{Math.random() * 360}}deg)`;
            bubble.style.animationDelay = `${{Math.random() * 500}}ms`;
            document.body.appendChild(bubble);
            setTimeout(() => bubble.remove(), 4000);
        }}
    }};
    createBubbles(15);
}});
</script>

</body>
</html>
"""
    return full_html


import shutil
import os

def save_and_open_report(html_content):
    # 确保报告目录存在
    if not os.path.exists(HTML_OUTPUT_DIR):
        os.makedirs(HTML_OUTPUT_DIR)
    
    # 复制xlsx.full.min.js到报告目录
    js_source = os.path.join(os.path.dirname(__file__), 'xlsx.full.min.js')
    js_destination = os.path.join(HTML_OUTPUT_DIR, 'xlsx.full.min.js')
    shutil.copy2(js_source, js_destination)

    if not os.path.exists(HTML_OUTPUT_DIR):
        os.makedirs(HTML_OUTPUT_DIR)

    with open(HTML_FILEPATH, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✅ Report generated: {HTML_FILEPATH}")
    webbrowser.open(HTML_FILEPATH)

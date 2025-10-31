# 输出路径
$htmlFile = "C:\Temp\AutoMakringReport.html"
if (-not (Test-Path (Split-Path $htmlFile))) { 
    New-Item -Path (Split-Path $htmlFile) -ItemType Directory -Force | Out-Null 
}

# 初始化 HTML
$global:html = @"
<html>
<head>
<meta charset='UTF-8'>
<title>评分结果检查报告</title>
<style>
body {
    font-family: "Segoe UI", Arial, sans-serif;
    background: linear-gradient(135deg, #e3f2fd, #f8f9fa);
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 30px;
}
h1 {
    color: #222;
    text-align: center;
}
.card {
    width: 60%;
    background: white;
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    margin: 15px;
    padding: 20px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.card:hover {
    transform: scale(1.02);
    box-shadow: 0 8px 20px rgba(0,0,0,0.2);
}
.ok { border: 3px solid #4CAF50; }
.fail { border: 3px solid #f44336; }
.question-title { font-size: 18px; color: #0078d7; font-weight: bold; }
.status { font-size: 16px; margin-top: 8px; }
.score { font-size: 14px; color: #333; margin-top: 6px; }
.raw-output { 
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
}
.final {
    width: 65%;
    text-align: center;
    font-size: 22px;
    font-weight: bold;
    padding: 25px;
    border-radius: 20px;
    background-color: #fff;
    box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    margin-top: 40px;
}
button {
    margin-top: 10px;
    padding: 6px 12px;
    font-size: 13px;
    border-radius: 8px;
    border: none;
    cursor: pointer;
    transition: 0.2s;
}
button.correct { background-color: #4CAF50; color: white; }
button.wrong { background-color: #f44336; color: white; margin-left: 8px; }
button:hover { opacity: 0.8; }
</style>
</head>
<body>
<h1>$(hostname) 评分结果检查报告 - $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")</h1>

<script>
function updateScore() {
    var total = 0;
    var max = 0;
    document.querySelectorAll('.card').forEach(function(card){
        var score = parseInt(card.getAttribute('data-score'));
        var passed = card.classList.contains('ok');
        max += score;
        if (passed) total += score;
    });
    document.getElementById('final-score').innerText = '最终得分：' + total + ' / 总分：' + max;
}

function markCard(el, passed) {
    var card = el.closest('.card');
    card.classList.remove('ok', 'fail');
    var status = card.querySelector('.status b');
    if (passed) {
        card.classList.add('ok');
        status.innerText = '✅ 已确认正确';
        status.style.color = '#4CAF50';
    } else {
        card.classList.add('fail');
        status.innerText = '❌ 已确认错误';
        status.style.color = '#f44336';
    }
    updateScore();
}
</script>
"@

# 分数统计
$global:TotalScore = 0
$global:MaxScore = 0
$global:QuestionIndex = 0

function Add-Card {
    param(
        [string]$Title,
        [string]$StatusText,
        [bool]$Passed,
        [int]$Score,
        [string]$RawOutput = ""
    )
    $global:QuestionIndex++
    $global:MaxScore += $Score
    $Earned = if ($Passed) { $Score } else { 0 }
    $global:TotalScore += $Earned
    $borderClass = if ($Passed) { "ok" } else { "fail" }
    $statusColor = if ($Passed) { "#4CAF50" } else { "#f44336" }

    $rawSection = ""
    if ($RawOutput -ne "") {
        $rawSection = "<div class='raw-output'><pre>$RawOutput</pre></div>"
    }

    $global:html += @"
<div class='card $borderClass' data-score='$Score'>
    <div class='question-title'>$($global:QuestionIndex). $Title</div>
    <div class='status'><b style='color:$statusColor;'>$StatusText</b></div>
    <div class='score'>得分：$Earned / 配分：$Score</div>
    <div>
        <button class='correct' onclick='markCard(this, true)'>确认正确 ✅</button>
        <button class='wrong' onclick='markCard(this, false)'>确认错误 ❌</button>
    </div>
    $rawSection
</div>
"@
}

# 🧩 检查 DNS Root Hints
try {
    $rootHintsObj = Get-DnsServerRootHint -ErrorAction SilentlyContinue
    $rawHints = ($rootHintsObj | Out-String)

    if ($rawHints -match "209\.45\.67\.254" -and $rawHints -match "ISP_RT") {
        Add-Card -Title "DNS Root Hint 配置" -StatusText "✅ Root Hint 正确" -Passed $true -Score 5 -RawOutput $rawHints
    } else {
        Add-Card -Title "DNS Root Hint 配置" -StatusText "❌ Root Hint 配置错误" -Passed $false -Score 5 -RawOutput $rawHints
    }
} catch {
    Add-Card -Title "DNS Root Hint 配置" -StatusText "❌ 检测失败" -Passed $false -Score 5 -RawOutput $rawHints
}

# 🧩 检查 Domain 回收站
try {
    $recycleBinFeature = Get-ADOptionalFeature -Filter {Name -eq "Recycle Bin Feature"} -ErrorAction SilentlyContinue | Select-Object IsDisableable
    $rawRecycleBinFeature = $recycleBinFeature | Out-String

    if ($rawRecycleBinFeature -match "False") {
        Add-Card -Title "Domain 回收站" -StatusText "✅ 已启用域回收站" -Passed $true -Score 5 -RawOutput $rawRecycleBinFeature
    } else {
        Add-Card -Title "Domain 回收站" -StatusText "❌ 未启用域回收站" -Passed $false -Score 5 -RawOutput $rawRecycleBinFeature
    }
} catch {
    $err = $_ | Out-String
    Add-Card -Title "Domain 回收站" -StatusText "❌ 检测失败（异常）" -Passed $false -Score 5 -RawOutput $err
}

# 🧩 检查 主机名称
try {
    $checkHostname = hostname
    $rawcheckHostname = $checkHostname | Out-String

    if ($rawcheckHostname -match "DC") {
        Add-Card -Title "主机名称" -StatusText "✅ 已修改主机名称" -Passed $true -Score 5 -RawOutput $rawcheckHostname
    } else {
        Add-Card -Title "主机名称" -StatusText "❌ 未修改主机名称" -Passed $false -Score 5 -RawOutput $rawcheckHostname
    }
} catch {
    $err = $_ | Out-String
    Add-Card -Title "主机名称" -StatusText "❌ 检测失败（异常）" -Passed $false -Score 5 -RawOutput $err
}

# 🏁 最终成绩卡片
$global:html += @"
<div class='final' id='final-score'>
最终得分：$($global:TotalScore) / 总分：$($global:MaxScore)
</div>
</body></html>
"@

# 输出
$global:html | Out-File -FilePath $htmlFile -Encoding UTF8
Write-Host "✅ 报告已生成: $htmlFile" -ForegroundColor Green
Start-Process $htmlFile

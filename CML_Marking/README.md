# CML Marking Script

## 概述
这是一个自动化网络设备配置检查和评分脚本，能够连接网络设备、执行配置检查并生成可视化报告。

## 功能特点
- 从Excel配置文件加载检查项
- 自动连接网络设备并执行命令检查
- 生成美观的HTML评分报告
- 支持错误处理和连接重试机制
- 精确的分数计算和结果展示

## 环境要求
- Python 3.8+ 
- Windows操作系统
- 网络设备访问权限

## 安装步骤
1. 克隆或下载项目到本地
2. 进入项目目录
```powershell
cd CML_Marking
```
3. 创建并激活虚拟环境
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```
4. 安装依赖包
```powershell
pip install -r requirements.txt
```

## 配置说明
1. **Excel配置文件**：编辑`check_configuration.xlsx`文件，添加或修改检查项
   - check_name: 检查项名称
   - command: 要执行的命令
   - expected_values: 预期结果
   - score: 该项分值
   - note: 检查说明

2. **环境配置**：修改`config.py`文件设置以下参数
   - CML_CONTROLLER: 控制器地址
   - CML_USERNAME: 用户名
   - CML_PASSWORD: 密码
   - ENABLE_SECRET: 特权模式密码
   - LAB_NAME: 实验名称

## 使用方法
1. 确保虚拟环境已激活
2. 运行主脚本
```powershell
python main.py
```
3. 脚本执行完成后，会自动打开生成的HTML报告

## 报告说明
- 报告保存在`html_reports`目录下
- 报告名称格式：AutoMakringReport_YYYYMMDD_HHMMSS.html
- 包含每个检查项的详细结果和得分情况
- 底部显示总分和满分

## 故障排除
- **连接错误**：检查网络连接和设备凭证
- **Excel文件错误**：确保文件格式正确且路径无误
- **依赖问题**：重新安装依赖包`pip install -r requirements.txt`

## 项目结构
```
CML_Marking/
├── check_configuration.xlsx  # 检查项配置文件
├── config.py                 # 环境配置
├── main.py                   # 主程序入口
├── network_connector.py      # 网络连接模块
├── report_generator.py       # 报告生成模块
├── requirements.txt          # 依赖包列表
├── utils.py                  # 工具函数
└── html_reports/             # 报告输出目录
```
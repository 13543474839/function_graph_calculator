"""打包脚本：运行 python build.py 生成 release/ 文件夹"""
import os
import re
import shutil

RELEASE_DIR = "release"

# 1. 清理旧的发布包
if os.path.exists(RELEASE_DIR):
    shutil.rmtree(RELEASE_DIR)
os.makedirs(RELEASE_DIR)

# 2. 读取最新的 HTML（从 static/index.html）
with open("static/index.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# 3. 读取 api.py 模板，替换 HTML 占位符
with open("api.py", "r", encoding="utf-8") as f:
    api_code = f.read()

# 将 API_BASE 从 "http://localhost:8000" 改为 ""（同源访问）
html_content = html_content.replace(
    'const API_BASE = "http://localhost:8000";',
    'const API_BASE = "";'
)

# 替换 api.py 中的 {{HTML_PLACEHOLDER}} 为真实 HTML
api_code = api_code.replace("{{HTML_PLACEHOLDER}}", html_content)

# 4. 生成发布包中的 api.py
with open(f"{RELEASE_DIR}/api.py", "w", encoding="utf-8") as f:
    f.write(api_code)

# 5. 复制其他依赖文件
for filename in ["expr_parser.py", "sampler.py"]:
    shutil.copy2(filename, RELEASE_DIR)

# 6. 生成 requirements.txt（依赖清单）
with open(f"{RELEASE_DIR}/requirements.txt", "w") as f:
    f.write("fastapi\nuvicorn\n")

# 7. 生成启动脚本（Windows 和 Mac/Linux）
with open(f"{RELEASE_DIR}/启动.bat", "w", encoding="utf-8") as f:
    f.write("""@echo off
chcp 65001 >nul
echo ====================================
echo   图形计算器 - 数据可视化课程设计
echo ====================================
echo.
python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo 正在安装依赖...
    pip install -r requirements.txt
    echo.
)
echo 启动成功后请打开浏览器访问: http://localhost:8000
echo 按 Ctrl+C 停止
echo.
python -m uvicorn api:app --host 0.0.0.0 --port 8000
pause
""")

with open(f"{RELEASE_DIR}/启动.sh", "w", encoding="utf-8") as f:
    f.write("""#!/bin/bash
echo "===================================="
echo "  图形计算器 - 数据可视化课程设计"
echo "===================================="
echo ""
python3 -c "import fastapi" 2>/dev/null  # 修复：使用 python3
if [ $? -ne 0 ]; then
    echo "正在安装依赖..."
    pip3 install -r requirements.txt  # 修复：使用 pip3
    echo ""
fi
echo "启动成功后请打开浏览器访问: http://localhost:8000"
echo "按 Ctrl+C 停止"
echo ""
python3 -m uvicorn api:app --host 0.0.0.0 --port 8000  # 修复：使用 python3
""")


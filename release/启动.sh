#!/bin/bash
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

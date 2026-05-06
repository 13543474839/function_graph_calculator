@echo off
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

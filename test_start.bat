@echo off
title 测试启动脚本
echo 测试脚本开始执行...

:: 切换到脚本所在目录
cd /d "%~dp0"
echo 当前目录: %cd%

:: 检查Python
echo 检查Python...
python --version
if errorlevel 1 (
    echo Python未找到！
    pause
    exit /b 1
)

:: 检查app.py
echo 检查app.py文件...
if not exist "app.py" (
    echo app.py文件不存在！
    pause
    exit /b 1
)

:: 检查依赖
echo 检查依赖...
python -c "import gradio, markitdown" 2>nul
if errorlevel 1 (
    echo 依赖未安装，正在安装...
    pip install gradio markitdown[all]
    if errorlevel 1 (
        echo 依赖安装失败！
        pause
        exit /b 1
    )
)

echo 所有检查通过，启动应用...
python app.py

echo 应用程序已退出
pause 
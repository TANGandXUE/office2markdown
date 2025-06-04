@echo off
chcp 65001
title MarkItDown 文档转换器 - 一键安装启动

echo ========================================
echo    MarkItDown 文档转换器
echo    一键安装和启动脚本
echo ========================================
echo.

:: 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到Python
    echo 请先安装Python 3.12或更高版本
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✓ Python已安装
python --version

:: 检查conda是否安装
conda --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  警告: 未找到Conda，将使用系统Python环境
    set USE_CONDA=false
) else (
    echo ✓ Conda已安装
    conda --version
    set USE_CONDA=true
)

echo.
echo ========================================
echo 正在设置环境...
echo ========================================

if "%USE_CONDA%"=="true" (
    echo 📦 使用Conda创建环境...
    
    :: 检查环境是否已存在
    conda info --envs | findstr "markitdown" >nul
    if not errorlevel 1 (
        echo ✓ markitdown环境已存在
    ) else (
        echo 创建新的conda环境...
        conda create -n markitdown python=3.12 -y
        if errorlevel 1 (
            echo ❌ 创建conda环境失败
            pause
            exit /b 1
        )
    )
    
    echo 激活conda环境...
    call conda activate markitdown
    if errorlevel 1 (
        echo ❌ 激活conda环境失败
        pause
        exit /b 1
    )
) else (
    echo 📦 使用系统Python环境...
)

echo.
echo ========================================
echo 正在安装依赖包...
echo ========================================

echo 📥 安装Python依赖...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ 安装依赖失败，尝试升级pip...
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ 安装依赖最终失败
        pause
        exit /b 1
    )
)

echo ✓ 依赖安装完成

echo.
echo ========================================
echo 正在启动Web界面...
echo ========================================

echo 🚀 启动MarkItDown文档转换器...
echo.
echo 📋 使用说明:
echo    - Web界面将在浏览器中自动打开
echo    - 默认地址: http://localhost:7860
echo    - 按 Ctrl+C 停止服务器
echo.

:: 启动应用
python app.py

echo.
echo ========================================
echo 程序已退出
echo ========================================
pause 
@echo off
chcp 65001 >nul 2>&1
title 📄 MarkItDown 文档转换器
setlocal enabledelayedexpansion

:: 记录开始时间用于调试
echo [DEBUG] 脚本开始执行...

:: 设置颜色变量
set "GREEN=[92m"
set "YELLOW=[93m"
set "RED=[91m"
set "BLUE=[94m"
set "CYAN=[96m"
set "WHITE=[97m"
set "NC=[0m"

echo %CYAN%========================================%NC%
echo %CYAN%       📄 MarkItDown 文档转换器       %NC%
echo %CYAN%    智能文档转换 - 一键启动工具       %NC%
echo %CYAN%========================================%NC%
echo.

:: 检查是否已经在conda环境中
if defined CONDA_DEFAULT_ENV (
    if "%CONDA_DEFAULT_ENV%"=="markitdown" (
        echo %GREEN%✓ 已在markitdown环境中%NC%
        goto :start_app
    )
)

:: 检查Python是否安装
echo %BLUE%🔍 检查系统环境...%NC%
echo [DEBUG] 检查Python...
python --version >nul 2>&1
set PYTHON_CHECK=!errorlevel!
echo [DEBUG] Python检查结果: !PYTHON_CHECK!
if !PYTHON_CHECK! neq 0 (
    echo %RED%❌ 未找到Python%NC%
    echo %YELLOW%请先安装Python 3.12或更高版本%NC%
    echo %YELLOW%下载地址: https://www.python.org/downloads/%NC%
    echo.
    echo [DEBUG] Python未安装，脚本将暂停
    pause
    exit /b 1
)

echo %GREEN%✓ Python已安装%NC%

:: 检查conda是否安装
echo [DEBUG] 检查Conda...
conda --version >nul 2>&1
set CONDA_CHECK=!errorlevel!
echo [DEBUG] Conda检查结果: !CONDA_CHECK!
if !CONDA_CHECK! neq 0 (
    echo %YELLOW%⚠️  未找到Conda，将使用系统Python环境%NC%
    echo [DEBUG] 跳转到系统Python环境
    goto :use_system_python
) else (
    echo %GREEN%✓ Conda已安装%NC%
)

:: 检查markitdown环境是否存在
echo %BLUE%🔧 检查conda环境...%NC%
echo [DEBUG] 检查markitdown环境...
conda info --envs | findstr "markitdown" >nul 2>&1
set ENV_CHECK=!errorlevel!
echo [DEBUG] 环境检查结果: !ENV_CHECK!
if !ENV_CHECK! neq 0 (
    echo %YELLOW%📦 创建markitdown环境...%NC%
    echo [DEBUG] 创建conda环境...
    conda create -n markitdown python=3.12 -y
    set CREATE_RESULT=!errorlevel!
    echo [DEBUG] 环境创建结果: !CREATE_RESULT!
    if !CREATE_RESULT! neq 0 (
        echo %RED%❌ 创建conda环境失败%NC%
        echo [DEBUG] 环境创建失败，跳转到系统Python
        goto :use_system_python
    )
    echo %GREEN%✓ 环境创建成功%NC%
) else (
    echo %GREEN%✓ markitdown环境已存在%NC%
)

:: 激活conda环境
echo %BLUE%🚀 激活conda环境...%NC%
echo [DEBUG] 激活markitdown环境...
call conda activate markitdown
set ACTIVATE_RESULT=!errorlevel!
echo [DEBUG] 环境激活结果: !ACTIVATE_RESULT!
if !ACTIVATE_RESULT! neq 0 (
    echo %RED%❌ 激活conda环境失败%NC%
    echo [DEBUG] 环境激活失败，跳转到系统Python
    goto :use_system_python
)

echo %GREEN%✓ 环境激活成功%NC%
goto :check_dependencies

:use_system_python
echo %YELLOW%📦 使用系统Python环境...%NC%
echo [DEBUG] 进入系统Python环境分支

:check_dependencies
:: 检查依赖是否已安装
echo %BLUE%📋 检查项目依赖...%NC%
python -c "import gradio, markitdown" >nul 2>&1
if errorlevel 1 (
    echo %YELLOW%📥 安装项目依赖...%NC%
    echo %CYAN%这可能需要几分钟时间，请耐心等待...%NC%
    echo.
    
    :: 先升级pip
    python -m pip install --upgrade pip --quiet
    
    :: 安装依赖
    pip install -r requirements.txt --quiet
    if errorlevel 1 (
        echo %RED%❌ 依赖安装失败%NC%
        echo %YELLOW%正在尝试逐个安装关键依赖...%NC%
        pip install gradio --quiet
        pip install "markitdown[all]" --quiet
        if errorlevel 1 (
            echo %RED%❌ 关键依赖安装失败，请检查网络连接%NC%
            pause
            exit /b 1
        )
    )
    echo %GREEN%✓ 依赖安装完成%NC%
) else (
    echo %GREEN%✓ 依赖已安装%NC%
)

:start_app
echo.
echo %CYAN%========================================%NC%
echo %CYAN%           🚀 启动Web服务器           %NC%
echo %CYAN%========================================%NC%
echo.
echo %GREEN%🌐 启动MarkItDown文档转换器...%NC%
echo.
echo %YELLOW%📋 使用说明:%NC%
echo %WHITE%   1. Web界面将自动在浏览器中打开%NC%
echo %WHITE%   2. 访问地址: %CYAN%http://localhost:7860%NC%
echo %WHITE%   3. 支持格式: docx, doc, pdf, pptx, xlsx, html%NC%
echo %WHITE%   4. 按 %RED%Ctrl+C%WHITE% 停止服务器%NC%
echo.
echo %CYAN%========================================%NC%
echo.

:: 启动应用（浏览器将由Python代码自动打开）
echo [DEBUG] 准备启动Python应用...
cd /d "%~dp0"
echo [DEBUG] 当前目录: %cd%
echo [DEBUG] 检查app.py文件...
if not exist "app.py" (
    echo %RED%❌ 找不到app.py文件%NC%
    echo [DEBUG] app.py文件不存在
    echo %YELLOW%请确保此脚本与app.py在同一目录中%NC%
    pause
    exit /b 1
)
echo [DEBUG] 启动应用程序...
python app.py
set APP_RESULT=!errorlevel!
echo [DEBUG] 应用程序退出，返回值: !APP_RESULT!

:: 程序结束后的处理
echo.
echo %CYAN%========================================%NC%
echo %GREEN%           程序已安全退出            %NC%
echo %CYAN%========================================%NC%
echo.
echo %YELLOW%💡 提示: 下次直接双击此文件即可启动%NC%
echo.
pause
goto :eof

:: 安装Miniconda的函数
:install_miniconda
echo %YELLOW%📦 正在下载并安装Miniconda...%NC%
echo %CYAN%这是一次性操作，安装后将大大简化环境管理%NC%
echo.

:: 创建临时目录
set "TEMP_DIR=%TEMP%\markitdown_setup"
if not exist "%TEMP_DIR%" mkdir "%TEMP_DIR%"

:: 下载Miniconda
set "MINICONDA_URL=https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe"
set "MINICONDA_FILE=%TEMP_DIR%\Miniconda3-latest-Windows-x86_64.exe"

echo %BLUE%📥 下载Miniconda安装程序...%NC%
powershell -Command "& {Invoke-WebRequest -Uri '%MINICONDA_URL%' -OutFile '%MINICONDA_FILE%'}" >nul 2>&1
if errorlevel 1 (
    echo %RED%❌ 下载失败，请检查网络连接%NC%
    exit /b 1
)

echo %BLUE%🔧 安装Miniconda...%NC%
"%MINICONDA_FILE%" /InstallationType=JustMe /RegisterPython=0 /S /D=%USERPROFILE%\Miniconda3
if errorlevel 1 (
    echo %RED%❌ Miniconda安装失败%NC%
    exit /b 1
)

:: 添加conda到PATH
set "PATH=%USERPROFILE%\Miniconda3;%USERPROFILE%\Miniconda3\Scripts;%PATH%"

:: 清理临时文件
del "%MINICONDA_FILE%" >nul 2>&1

echo %GREEN%✓ Miniconda安装完成%NC%
exit /b 0 
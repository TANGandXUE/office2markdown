#!/bin/bash

# MarkItDown 文档转换器 - 一键安装启动脚本

set -e  # 遇到错误时退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_message() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

print_message $BLUE "========================================"
print_message $BLUE "   MarkItDown 文档转换器"
print_message $BLUE "   一键安装和启动脚本"
print_message $BLUE "========================================"
echo

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        print_message $RED "❌ 错误: 未找到Python"
        print_message $YELLOW "请先安装Python 3.12或更高版本"
        print_message $YELLOW "下载地址: https://www.python.org/downloads/"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

print_message $GREEN "✓ Python已安装"
$PYTHON_CMD --version

# 检查pip
if ! command -v pip3 &> /dev/null; then
    if ! command -v pip &> /dev/null; then
        print_message $RED "❌ 错误: 未找到pip"
        exit 1
    else
        PIP_CMD="pip"
    fi
else
    PIP_CMD="pip3"
fi

# 检查conda是否安装
USE_CONDA=false
if command -v conda &> /dev/null; then
    print_message $GREEN "✓ Conda已安装"
    conda --version
    USE_CONDA=true
else
    print_message $YELLOW "⚠️  警告: 未找到Conda，将使用系统Python环境"
fi

echo
print_message $BLUE "========================================"
print_message $BLUE "正在设置环境..."
print_message $BLUE "========================================"

if [ "$USE_CONDA" = true ]; then
    print_message $BLUE "📦 使用Conda创建环境..."
    
    # 检查环境是否已存在
    if conda info --envs | grep -q "markitdown"; then
        print_message $GREEN "✓ markitdown环境已存在"
    else
        print_message $YELLOW "创建新的conda环境..."
        conda create -n markitdown python=3.12 -y
    fi
    
    print_message $YELLOW "激活conda环境..."
    # 激活conda环境
    eval "$(conda shell.bash hook)"
    conda activate markitdown
    
    PYTHON_CMD="python"
    PIP_CMD="pip"
else
    print_message $BLUE "📦 使用系统Python环境..."
fi

echo
print_message $BLUE "========================================"
print_message $BLUE "正在安装依赖包..."
print_message $BLUE "========================================"

print_message $YELLOW "📥 安装Python依赖..."
if ! $PIP_CMD install -r requirements.txt; then
    print_message $YELLOW "❌ 安装依赖失败，尝试升级pip..."
    $PYTHON_CMD -m pip install --upgrade pip
    $PIP_CMD install -r requirements.txt
fi

print_message $GREEN "✓ 依赖安装完成"

echo
print_message $BLUE "========================================"
print_message $BLUE "正在启动Web界面..."
print_message $BLUE "========================================"

print_message $GREEN "🚀 启动MarkItDown文档转换器..."
echo
print_message $YELLOW "📋 使用说明:"
print_message $YELLOW "   - Web界面将在浏览器中自动打开"
print_message $YELLOW "   - 默认地址: http://localhost:7860"
print_message $YELLOW "   - 按 Ctrl+C 停止服务器"
echo

# 启动应用
$PYTHON_CMD app.py

echo
print_message $BLUE "========================================"
print_message $BLUE "程序已退出"
print_message $BLUE "========================================" 
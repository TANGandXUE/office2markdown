#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MarkItDown 文档转换测试脚本
用于将docx、doc等文件转换为markdown格式
"""

from markitdown import MarkItDown
import os
import sys

def convert_document(input_file, output_file=None):
    """
    转换文档文件为markdown格式
    
    Args:
        input_file (str): 输入文件路径
        output_file (str, optional): 输出文件路径，如果不指定则自动生成
    """
    try:
        # 创建MarkItDown实例
        markitdown = MarkItDown()
        
        # 检查输入文件是否存在
        if not os.path.exists(input_file):
            print(f"错误：文件 '{input_file}' 不存在")
            return False
        
        print(f"正在转换文件：{input_file}")
        
        # 执行转换
        result = markitdown.convert(input_file)
        
        # 如果没有指定输出文件，自动生成
        if output_file is None:
            base_name = os.path.splitext(input_file)[0]
            output_file = f"{base_name}.md"
        
        # 写入转换结果
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result.text_content)
        
        print(f"转换成功！输出文件：{output_file}")
        print(f"内容预览（前200字符）：")
        print("-" * 40)
        print(result.text_content[:200] + "..." if len(result.text_content) > 200 else result.text_content)
        print("-" * 40)
        
        return True
        
    except Exception as e:
        print(f"转换失败：{str(e)}")
        return False

def list_convertible_files():
    """列出当前目录下可转换的文件"""
    print("当前目录下的可转换文件：")
    print("-" * 40)
    
    supported_extensions = ['.docx', '.doc', '.pdf', '.pptx', '.xlsx', '.html', '.htm']
    files_found = []
    
    for file in os.listdir('.'):
        if any(file.lower().endswith(ext) for ext in supported_extensions):
            files_found.append(file)
            print(f"  {file}")
    
    if not files_found:
        print("  没有找到支持的文件格式")
    
    print("-" * 40)
    return files_found

def main():
    """主函数"""
    print("MarkItDown 文档转换工具")
    print("支持格式：docx, doc, pdf, pptx, xlsx, html 等")
    print("=" * 50)
    
    # 列出可转换的文件
    files = list_convertible_files()
    
    if not files:
        print("请确保当前目录有支持的文档文件")
        return
    
    # 如果有命令行参数，使用第一个参数作为输入文件
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        convert_document(input_file, output_file)
    else:
        print("\n使用方法：")
        print("1. python test_conversion.py <输入文件> [输出文件]")
        print("2. 或者直接运行此脚本查看可转换的文件列表")
        print("\n示例：")
        for file in files[:3]:  # 只显示前3个文件作为示例
            base_name = os.path.splitext(file)[0]
            print(f"  python test_conversion.py \"{file}\" \"{base_name}.md\"")

if __name__ == "__main__":
    main() 
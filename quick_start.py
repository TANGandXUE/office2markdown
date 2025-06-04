#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MarkItDown 快速使用指南
最简单的文档转换示例
"""

from markitdown import MarkItDown
import os

def quick_convert_demo():
    """快速转换演示"""
    print("=== MarkItDown 快速转换工具 ===")
    print()
    
    # 创建转换器
    md = MarkItDown()
    
    # 列出当前目录的Word文档
    word_files = [f for f in os.listdir('.') if f.endswith(('.docx', '.doc'))]
    
    if not word_files:
        print("当前目录没有找到Word文档文件")
        return
    
    print(f"发现 {len(word_files)} 个Word文档:")
    for i, file in enumerate(word_files, 1):
        print(f"{i}. {file}")
    
    print()
    print("选择要转换的文件 (输入数字，或按回车转换全部):")
    choice = input().strip()
    
    if choice == "":
        # 转换全部文件
        files_to_convert = word_files
    else:
        try:
            index = int(choice) - 1
            if 0 <= index < len(word_files):
                files_to_convert = [word_files[index]]
            else:
                print("无效的选择")
                return
        except ValueError:
            print("请输入有效的数字")
            return
    
    # 执行转换
    print()
    for file in files_to_convert:
        print(f"正在转换: {file}")
        try:
            result = md.convert(file)
            
            # 生成输出文件名
            output_file = os.path.splitext(file)[0] + ".md"
            
            # 保存转换结果
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(result.text_content)
            
            print(f"✓ 转换成功: {output_file}")
            
            # 显示简短预览
            preview = result.text_content[:100].replace('\n', ' ')
            if len(result.text_content) > 100:
                preview += "..."
            print(f"  预览: {preview}")
            
        except Exception as e:
            print(f"✗ 转换失败: {str(e)}")
        
        print("-" * 40)
    
    print("转换完成！")

if __name__ == "__main__":
    quick_convert_demo() 
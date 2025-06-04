#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MarkItDown 批量文档转换脚本
用于批量将docx、doc等文件转换为markdown格式
"""

from markitdown import MarkItDown
import os
import sys
import shutil
from pathlib import Path

class DocumentConverter:
    def __init__(self, output_dir="markdown_output"):
        """
        初始化转换器
        
        Args:
            output_dir (str): 输出目录名称
        """
        self.markitdown = MarkItDown()
        self.output_dir = output_dir
        self.supported_extensions = ['.docx', '.doc', '.pdf', '.pptx', '.xlsx', '.html', '.htm']
        
        # 创建输出目录
        Path(output_dir).mkdir(exist_ok=True)
        print(f"输出目录：{os.path.abspath(output_dir)}")
    
    def is_supported_file(self, filename):
        """检查文件是否为支持的格式"""
        return any(filename.lower().endswith(ext) for ext in self.supported_extensions)
    
    def convert_single_file(self, input_file):
        """
        转换单个文件
        
        Args:
            input_file (str): 输入文件路径
            
        Returns:
            bool: 转换是否成功
        """
        try:
            print(f"\n正在转换：{input_file}")
            
            # 执行转换
            result = self.markitdown.convert(input_file)
            
            # 生成输出文件名
            base_name = Path(input_file).stem
            output_file = os.path.join(self.output_dir, f"{base_name}.md")
            
            # 写入转换结果
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(result.text_content)
            
            print(f"✓ 转换成功：{output_file}")
            
            # 显示简短预览
            preview = result.text_content[:150].replace('\n', ' ')
            if len(result.text_content) > 150:
                preview += "..."
            print(f"  内容预览: {preview}")
            
            return True
            
        except Exception as e:
            print(f"✗ 转换失败：{input_file}")
            print(f"  错误信息：{str(e)}")
            return False
    
    def convert_all_files(self, directory="."):
        """
        转换目录中的所有支持文件
        
        Args:
            directory (str): 要搜索的目录
        """
        files_to_convert = []
        
        # 查找所有支持的文件
        for file in os.listdir(directory):
            if self.is_supported_file(file):
                files_to_convert.append(file)
        
        if not files_to_convert:
            print("没有找到支持的文件格式")
            return
        
        print(f"找到 {len(files_to_convert)} 个文件需要转换：")
        for file in files_to_convert:
            print(f"  - {file}")
        
        print("\n开始批量转换...")
        print("=" * 60)
        
        success_count = 0
        for file in files_to_convert:
            if self.convert_single_file(file):
                success_count += 1
        
        print("=" * 60)
        print(f"批量转换完成！")
        print(f"成功转换：{success_count}/{len(files_to_convert)} 个文件")
        print(f"输出目录：{os.path.abspath(self.output_dir)}")
    
    def convert_specific_files(self, file_list):
        """
        转换指定的文件列表
        
        Args:
            file_list (list): 要转换的文件列表
        """
        existing_files = [f for f in file_list if os.path.exists(f)]
        
        if not existing_files:
            print("指定的文件都不存在")
            return
        
        print(f"开始转换 {len(existing_files)} 个指定文件...")
        print("=" * 60)
        
        success_count = 0
        for file in existing_files:
            if self.convert_single_file(file):
                success_count += 1
        
        print("=" * 60)
        print(f"转换完成！")
        print(f"成功转换：{success_count}/{len(existing_files)} 个文件")

def main():
    """主函数"""
    print("MarkItDown 批量文档转换工具")
    print("支持格式：docx, doc, pdf, pptx, xlsx, html 等")
    print("=" * 60)
    
    # 创建转换器实例
    converter = DocumentConverter()
    
    if len(sys.argv) > 1:
        # 如果提供了命令行参数，转换指定文件
        files_to_convert = sys.argv[1:]
        converter.convert_specific_files(files_to_convert)
    else:
        # 否则转换当前目录下的所有支持文件
        converter.convert_all_files()

if __name__ == "__main__":
    main() 
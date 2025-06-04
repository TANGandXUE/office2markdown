#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MarkItDown Web界面
基于Gradio的文档转换工具，支持批量转换和实时预览
"""

import gradio as gr
import os
import tempfile
import shutil
from pathlib import Path
from markitdown import MarkItDown
import zipfile
from typing import List, Tuple, Optional
import logging
import time

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentConverter:
    def __init__(self):
        """初始化转换器"""
        self.markitdown = MarkItDown()
        self.supported_extensions = ['.docx', '.doc', '.pdf', '.pptx', '.xlsx', '.html', '.htm']
        
    def is_supported_file(self, filename: str) -> bool:
        """检查文件是否为支持的格式"""
        return any(filename.lower().endswith(ext) for ext in self.supported_extensions)
    
    def convert_single_file(self, file_path: str) -> Tuple[bool, str, str]:
        """
        转换单个文件
        
        Returns:
            Tuple[bool, str, str]: (成功标志, markdown内容, 错误信息)
        """
        try:
            logger.info(f"开始转换文件: {file_path}")
            result = self.markitdown.convert(file_path)
            return True, result.text_content, ""
        except Exception as e:
            error_msg = f"转换失败: {str(e)}"
            logger.error(error_msg)
            return False, "", error_msg
    
    def convert_multiple_files(self, files: List[str]) -> Tuple[str, List[str]]:
        """
        批量转换文件
        
        Returns:
            Tuple[str, List[str]]: (zip文件路径, 转换日志)
        """
        logs = []
        success_count = 0
        
        # 创建临时目录
        temp_dir = tempfile.mkdtemp()
        output_dir = os.path.join(temp_dir, "converted_files")
        os.makedirs(output_dir, exist_ok=True)
        
        for file_path in files:
            if not self.is_supported_file(file_path):
                logs.append(f"❌ 跳过不支持的文件: {os.path.basename(file_path)}")
                continue
                
            success, content, error = self.convert_single_file(file_path)
            
            if success:
                # 生成输出文件名
                base_name = Path(file_path).stem
                output_file = os.path.join(output_dir, f"{base_name}.md")
                
                # 保存转换结果
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                logs.append(f"✅ 成功转换: {os.path.basename(file_path)} -> {base_name}.md")
                success_count += 1
            else:
                logs.append(f"❌ 转换失败: {os.path.basename(file_path)} - {error}")
        
        # 创建ZIP文件
        zip_path = os.path.join(temp_dir, "converted_documents.zip")
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(output_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, output_dir)
                    zipf.write(file_path, arcname)
        
        logs.append(f"\n📊 转换完成! 成功: {success_count}/{len(files)} 个文件")
        
        return zip_path, logs

# 全局转换器实例
converter = DocumentConverter()

def convert_single_document(file) -> Tuple[str, str]:
    """Gradio接口：转换单个文档"""
    if file is None:
        return "请上传一个文件", ""
    
    file_path = file.name
    filename = os.path.basename(file_path)
    
    if not converter.is_supported_file(filename):
        supported_formats = ", ".join(converter.supported_extensions)
        return f"不支持的文件格式。支持的格式: {supported_formats}", ""
    
    success, content, error = converter.convert_single_file(file_path)
    
    if success:
        preview = content[:500] + "..." if len(content) > 500 else content
        status = f"✅ 转换成功: {filename}\n文件大小: {len(content)} 字符"
        return status, content
    else:
        return f"❌ 转换失败: {filename}\n错误: {error}", ""

def convert_multiple_documents(files) -> Tuple[str, Optional[str]]:
    """Gradio接口：批量转换文档"""
    if not files:
        return "请上传至少一个文件", None
    
    file_paths = [f.name for f in files]
    
    zip_path, logs = converter.convert_multiple_files(file_paths)
    
    log_text = "\n".join(logs)
    
    return log_text, zip_path

def get_file_info(files) -> str:
    """获取上传文件的信息"""
    if not files:
        return "未选择文件"
    
    info_lines = ["📁 已选择的文件:"]
    supported_count = 0
    
    for file in files:
        filename = os.path.basename(file.name)
        file_size = os.path.getsize(file.name)
        size_mb = file_size / (1024 * 1024)
        
        if converter.is_supported_file(filename):
            status = "✅"
            supported_count += 1
        else:
            status = "❌"
        
        info_lines.append(f"{status} {filename} ({size_mb:.2f} MB)")
    
    info_lines.append(f"\n📊 支持的文件: {supported_count}/{len(files)}")
    
    return "\n".join(info_lines)

def create_interface():
    """创建Gradio界面"""
    
    # 自定义CSS
    custom_css = """
    .gradio-container {
        max-width: 1200px !important;
    }
    .file-info {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    }
    .success-text {
        color: #28a745;
    }
    .error-text {
        color: #dc3545;
    }
    """
    
    with gr.Blocks(
        title="📄 MarkItDown 文档转换器", 
        theme=gr.themes.Soft(),
        css=custom_css
    ) as demo:
        
        gr.Markdown("""
        # 📄 MarkItDown 文档转换器
        
        将 Office 文档转换为 Markdown 格式，支持实时预览和批量处理
        
        **支持格式**: docx, doc, pdf, pptx, xlsx, html, htm
        """)
        
        with gr.Tabs():
            # 单文件转换标签页
            with gr.TabItem("🔄 单文件转换"):
                with gr.Row():
                    with gr.Column(scale=1):
                        single_file_input = gr.File(
                            label="上传文档文件",
                            file_types=[".docx", ".doc", ".pdf", ".pptx", ".xlsx", ".html", ".htm"]
                        )
                        single_convert_btn = gr.Button("🚀 开始转换", variant="primary")
                        
                    with gr.Column(scale=2):
                        single_status = gr.Textbox(
                            label="转换状态",
                            lines=3,
                            interactive=False
                        )
                
                gr.Markdown("### 📖 转换结果预览")
                single_output = gr.Textbox(
                    label="Markdown 内容",
                    lines=15,
                    max_lines=20,
                    interactive=False,
                    show_copy_button=True
                )
                
                # 下载按钮
                single_download = gr.File(
                    label="下载 Markdown 文件",
                    visible=False
                )
            
            # 批量转换标签页
            with gr.TabItem("📁 批量转换"):
                with gr.Row():
                    with gr.Column(scale=1):
                        multi_file_input = gr.File(
                            label="上传多个文档文件",
                            file_count="multiple",
                            file_types=[".docx", ".doc", ".pdf", ".pptx", ".xlsx", ".html", ".htm"]
                        )
                        
                        file_info_display = gr.Textbox(
                            label="文件信息",
                            lines=8,
                            interactive=False,
                            elem_classes=["file-info"]
                        )
                        
                        multi_convert_btn = gr.Button("🚀 批量转换", variant="primary")
                    
                    with gr.Column(scale=1):
                        multi_status = gr.Textbox(
                            label="转换日志",
                            lines=15,
                            interactive=False
                        )
                        
                        multi_download = gr.File(
                            label="下载转换结果 (ZIP)",
                            visible=False
                        )
            
            # 关于标签页
            with gr.TabItem("ℹ️ 关于"):
                gr.Markdown("""
                ## 🛠️ 技术说明
                
                本工具基于 Microsoft 的 MarkItDown 项目构建：
                - **GitHub**: https://github.com/microsoft/markitdown
                - **版本**: 0.1.2
                - **核心功能**: 利用 AI 技术进行智能文档解析和转换
                
                ## 📋 使用说明
                
                ### 单文件转换
                1. 点击 "单文件转换" 标签页
                2. 上传一个支持的文档文件
                3. 点击 "开始转换" 按钮
                4. 查看转换结果和预览
                
                ### 批量转换
                1. 点击 "批量转换" 标签页
                2. 同时上传多个文档文件
                3. 查看文件信息确认支持情况
                4. 点击 "批量转换" 按钮
                5. 下载包含所有转换结果的 ZIP 文件
                
                ## ⚠️ 注意事项
                
                - **文件大小**: 建议单个文件不超过 50MB
                - **格式支持**: .docx 支持最佳，.doc 格式可能有兼容性问题
                - **复杂格式**: 表格、图片等复杂格式会尽力保持，但可能需要手动调整
                - **处理时间**: 大文件或批量文件可能需要较长处理时间
                
                ## 🔧 环境要求
                
                - Python 3.12+
                - MarkItDown[all] 包
                - Gradio 界面库
                """)
        
        # 事件绑定
        def save_single_result(content, filename="converted.md"):
            """保存单文件转换结果"""
            if not content.strip():
                return None
            
            temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8')
            temp_file.write(content)
            temp_file.close()
            return temp_file.name
        
        # 单文件转换事件
        single_convert_btn.click(
            fn=convert_single_document,
            inputs=[single_file_input],
            outputs=[single_status, single_output]
        )
        
        # 当有转换结果时，自动创建下载文件
        single_output.change(
            fn=lambda content: save_single_result(content) if content.strip() else None,
            inputs=[single_output],
            outputs=[single_download]
        )
        
        # 批量转换事件
        multi_file_input.change(
            fn=get_file_info,
            inputs=[multi_file_input],
            outputs=[file_info_display]
        )
        
        multi_convert_btn.click(
            fn=convert_multiple_documents,
            inputs=[multi_file_input],
            outputs=[multi_status, multi_download]
        )
    
    return demo

if __name__ == "__main__":
    # 创建并启动界面
    demo = create_interface()
    
    # 启动服务器
    demo.launch(
        server_name="0.0.0.0",  # 允许外部访问
        server_port=7860,       # 默认端口
        share=False,            # 不创建公共链接
        show_error=True,        # 显示错误信息
        quiet=False             # 显示启动信息
    ) 
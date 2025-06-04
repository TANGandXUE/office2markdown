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
import webbrowser
import threading
import subprocess
import sys

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
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
        return f"❌ 不支持的文件格式\n支持的格式: {supported_formats}", ""
    
    success, content, error = converter.convert_single_file(file_path)
    
    if success:
        char_count = len(content)
        word_count = len(content.split())
        line_count = len(content.split('\n'))
        
        status = f"""✅ 转换成功: {filename}
📊 统计信息:
   • 字符数: {char_count:,}
   • 单词数: {word_count:,}
   • 行数: {line_count:,}"""
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
        return "📂 未选择文件"
    
    info_lines = ["📁 已选择的文件:"]
    supported_count = 0
    total_size = 0
    
    for file in files:
        filename = os.path.basename(file.name)
        file_size = os.path.getsize(file.name)
        size_mb = file_size / (1024 * 1024)
        total_size += file_size
        
        if converter.is_supported_file(filename):
            status = "✅"
            supported_count += 1
        else:
            status = "❌"
        
        info_lines.append(f"  {status} {filename} ({size_mb:.2f} MB)")
    
    total_size_mb = total_size / (1024 * 1024)
    info_lines.append(f"\n📊 文件统计:")
    info_lines.append(f"  • 总文件数: {len(files)}")
    info_lines.append(f"  • 支持的文件: {supported_count}")
    info_lines.append(f"  • 总大小: {total_size_mb:.2f} MB")
    
    return "\n".join(info_lines)

def save_single_result(content, filename="converted_document.md"):
    """保存单文件转换结果"""
    if not content.strip():
        return None
    
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8')
    temp_file.write(content)
    temp_file.close()
    return temp_file.name

def create_interface():
    """创建Gradio界面"""
    
    # 自定义CSS
    custom_css = """
    .gradio-container {
        max-width: 1400px !important;
        margin: 0 auto !important;
    }
    .file-info {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .status-success {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        border-radius: 8px;
        padding: 15px;
    }
    .status-error {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        border-radius: 8px;
        padding: 15px;
    }
    .main-header {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 30px;
    }
    """
    
    with gr.Blocks(
        title="📄 MarkItDown 文档转换器", 
        theme=gr.themes.Soft(
            primary_hue="blue",
            secondary_hue="cyan",
            neutral_hue="slate"
        ),
        css=custom_css
    ) as demo:
        
        # 主标题
        gr.HTML("""
        <div class="main-header">
            <h1>📄 MarkItDown 文档转换器</h1>
            <p>智能文档转换工具 • 支持批量处理 • 实时预览</p>
            <p><strong>支持格式:</strong> docx, doc, pdf, pptx, xlsx, html, htm</p>
        </div>
        """)
        
        with gr.Tabs() as tabs:
            # 单文件转换标签页
            with gr.TabItem("🔄 单文件转换", elem_id="single-tab"):
                with gr.Row():
                    with gr.Column(scale=2):
                        single_file_input = gr.File(
                            label="📎 上传文档文件",
                            file_types=[".docx", ".doc", ".pdf", ".pptx", ".xlsx", ".html", ".htm"],
                            height=150
                        )
                        
                        with gr.Row():
                            single_convert_btn = gr.Button(
                                "🚀 开始转换", 
                                variant="primary", 
                                size="lg",
                                scale=2
                            )
                            single_clear_btn = gr.Button(
                                "🗑️ 清除", 
                                variant="secondary",
                                scale=1
                            )
                        
                    with gr.Column(scale=3):
                        single_status = gr.Textbox(
                            label="📊 转换状态",
                            lines=6,
                            interactive=False,
                            elem_classes=["file-info"]
                        )
                
                gr.Markdown("### 📖 转换结果预览")
                single_output = gr.Textbox(
                    label="Markdown 内容",
                    lines=20,
                    max_lines=25,
                    interactive=False,
                    show_copy_button=True,
                    placeholder="转换结果将在这里显示..."
                )
                
                single_download = gr.File(
                    label="💾 下载 Markdown 文件",
                    visible=False
                )
            
            # 批量转换标签页
            with gr.TabItem("📁 批量转换", elem_id="batch-tab"):
                with gr.Row():
                    with gr.Column(scale=2):
                        multi_file_input = gr.File(
                            label="📎 上传多个文档文件",
                            file_count="multiple",
                            file_types=[".docx", ".doc", ".pdf", ".pptx", ".xlsx", ".html", ".htm"],
                            height=200
                        )
                        
                        file_info_display = gr.Textbox(
                            label="📋 文件信息",
                            lines=12,
                            interactive=False,
                            elem_classes=["file-info"],
                            placeholder="选择文件后将显示详细信息..."
                        )
                        
                        with gr.Row():
                            multi_convert_btn = gr.Button(
                                "🚀 批量转换", 
                                variant="primary", 
                                size="lg",
                                scale=2
                            )
                            multi_clear_btn = gr.Button(
                                "🗑️ 清除", 
                                variant="secondary",
                                scale=1
                            )
                    
                    with gr.Column(scale=2):
                        multi_status = gr.Textbox(
                            label="📊 转换日志",
                            lines=20,
                            interactive=False,
                            elem_classes=["file-info"],
                            placeholder="转换日志将在这里显示..."
                        )
                        
                        multi_download = gr.File(
                            label="💾 下载转换结果 (ZIP)",
                            visible=False
                        )
            
            # 使用帮助标签页
            with gr.TabItem("❓ 使用帮助", elem_id="help-tab"):
                gr.Markdown("""
                ## 🎯 快速上手指南
                
                ### 🔄 单文件转换
                1. **上传文件**: 点击上传区域或拖拽文件到指定位置
                2. **开始转换**: 点击"开始转换"按钮
                3. **查看结果**: 在预览区域查看转换后的Markdown内容
                4. **下载文件**: 点击下载按钮保存.md文件
                
                ### 📁 批量转换
                1. **选择多个文件**: 同时上传多个文档（支持拖拽）
                2. **检查文件信息**: 确认文件格式和大小
                3. **批量转换**: 点击"批量转换"按钮
                4. **下载ZIP包**: 获取包含所有转换结果的压缩包
                
                ## 📋 支持格式详情
                
                | 格式 | 扩展名 | 转换质量 | 说明 |
                |------|--------|----------|------|
                | **Word文档** | `.docx` | ⭐⭐⭐⭐⭐ | 完美支持，推荐格式 |
                | **Word文档** | `.doc` | ⭐⭐⭐ | 基本支持，可能有兼容性问题 |
                | **PDF文档** | `.pdf` | ⭐⭐⭐⭐ | 文本PDF支持良好 |
                | **PowerPoint** | `.pptx` | ⭐⭐⭐⭐ | 幻灯片内容转换 |
                | **Excel表格** | `.xlsx` | ⭐⭐⭐⭐ | 表格数据转换 |
                | **网页文件** | `.html`, `.htm` | ⭐⭐⭐⭐⭐ | 完美支持 |
                
                ## ⚡ 性能优化建议
                
                - **文件大小**: 建议单个文件不超过 50MB
                - **批量处理**: 建议同时处理的文件数量不超过 20个
                - **网络要求**: 首次使用需要联网下载依赖包
                - **内存使用**: 大文件转换时建议关闭其他程序
                
                ## ⚠️ 注意事项
                
                ### 文档质量
                - 复杂的表格和图片可能需要手动调整
                - 公式和特殊符号转换效果因文档而异
                - 建议转换后检查重要内容的完整性
                
                ### 隐私安全
                - 所有转换操作在本地进行，不会上传到外部服务器
                - 临时文件会在处理完成后自动清理
                - 建议在安全的网络环境中使用
                
                ## 🐛 故障排除
                
                ### 常见问题
                
                **Q: 转换失败怎么办？**
                - 检查文件是否损坏
                - 确认文件格式是否支持
                - 查看错误信息获取具体原因
                
                **Q: 转换速度慢？**
                - 大文件转换需要更多时间
                - 检查系统资源使用情况
                - 尝试重启程序释放内存
                
                **Q: 无法打开网页？**
                - 确认地址是 http://localhost:7860
                - 检查防火墙设置
                - 尝试使用不同的浏览器
                
                ## 🔧 技术支持
                
                如需技术支持，请提供以下信息：
                - 操作系统版本
                - Python版本
                - 错误日志信息
                - 问题文件类型和大小
                """)
        
        # 事件绑定
        
        # 单文件转换事件
        single_convert_btn.click(
            fn=convert_single_document,
            inputs=[single_file_input],
            outputs=[single_status, single_output]
        )
        
        # 自动生成下载文件
        single_output.change(
            fn=lambda content: save_single_result(content) if content and content.strip() else None,
            inputs=[single_output],
            outputs=[single_download]
        )
        
        # 单文件清除按钮
        single_clear_btn.click(
            fn=lambda: (None, "", "", None),
            outputs=[single_file_input, single_status, single_output, single_download]
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
        
        # 批量清除按钮
        multi_clear_btn.click(
            fn=lambda: (None, "", "", None),
            outputs=[multi_file_input, file_info_display, multi_status, multi_download]
        )
    
    return demo

def open_browser():
    """延迟打开浏览器"""
    time.sleep(4)  # 等待服务器启动
    
    url = "http://localhost:7860"
    print("🌐 正在打开浏览器...")
    
    try:
        # 优先使用Windows系统命令
        if sys.platform == "win32":
            subprocess.run(["start", url], shell=True, check=True)
            print("✅ 浏览器已启动 (系统命令)")
            return
    except Exception as e:
        print(f"⚠️ 系统命令失败: {e}")
    
    try:
        # 备用方案：使用webbrowser模块
        success = webbrowser.open(url)
        if success:
            print("✅ 浏览器已启动 (webbrowser)")
        else:
            print("❌ webbrowser.open返回False")
    except Exception as e:
        print(f"⚠️ webbrowser启动失败: {e}")
        
    # 如果都失败了，提示用户手动访问
    print(f"📋 如果浏览器未自动打开，请手动访问: {url}")

if __name__ == "__main__":
    print("🚀 正在启动 MarkItDown 文档转换器...")
    print("📱 Web界面地址: http://localhost:7860")
    print("⏹️  按 Ctrl+C 停止服务器")
    print("-" * 50)
    
    # 创建并启动界面
    demo = create_interface()
    
    # 在后台线程中打开浏览器
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # 启动服务器
    try:
        demo.launch(
            server_name="127.0.0.1",
            server_port=7860,
            share=False,
            show_error=True,
            quiet=False,
            show_api=False,
            favicon_path=None,
            ssl_verify=False,
            inbrowser=False  # 禁用gradio自动打开浏览器，使用我们的自定义方法
        )
    except KeyboardInterrupt:
        print("\n👋 感谢使用 MarkItDown 文档转换器！")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        input("按任意键退出...") 
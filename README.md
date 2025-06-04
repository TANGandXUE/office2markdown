# 📄 MarkItDown 文档转换器

> 基于Microsoft MarkItDown的智能文档转换工具，支持Web界面操作，一键部署使用

## ✨ 特性

- 🌐 **现代Web界面** - 基于Gradio构建的直观用户界面
- 📁 **批量转换** - 支持同时处理多个文档文件
- 🔄 **实时预览** - 即时查看转换结果
- 📦 **一键部署** - 自动安装依赖和启动服务
- 🎯 **智能识别** - AI驱动的文件格式检测
- 💾 **便捷下载** - 支持单文件和批量ZIP下载

## 📋 支持格式

| 格式类型 | 文件扩展名 | 支持程度 |
|---------|-----------|----------|
| **Word文档** | `.docx`, `.doc` | ✅ 完全支持 (.docx 最佳) |
| **PDF文档** | `.pdf` | ✅ 完全支持 |
| **PowerPoint** | `.pptx` | ✅ 完全支持 |
| **Excel表格** | `.xlsx` | ✅ 完全支持 |
| **网页文件** | `.html`, `.htm` | ✅ 完全支持 |

## 🚀 快速开始

### 方法一：一键启动 (推荐)

#### Windows用户
```bash
# 双击运行或在命令行执行
install_and_run.bat
```

#### Linux/Mac用户
```bash
# 给脚本执行权限
chmod +x install_and_run.sh

# 运行脚本
./install_and_run.sh
```

### 方法二：手动安装

1. **环境准备**
   ```bash
   # 使用Conda (推荐)
   conda create -n markitdown python=3.12 -y
   conda activate markitdown
   
   # 或使用venv
   python -m venv markitdown
   source markitdown/bin/activate  # Linux/Mac
   # markitdown\Scripts\activate   # Windows
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **启动应用**
   ```bash
   python app.py
   ```

4. **访问界面**
   
   打开浏览器访问：http://localhost:7860

## 🎯 使用指南

### 📱 Web界面操作

#### 🔄 单文件转换
1. 点击 **"单文件转换"** 标签页
2. 上传一个支持的文档文件
3. 点击 **"开始转换"** 按钮
4. 查看转换状态和Markdown预览
5. 复制内容或下载.md文件

#### 📁 批量转换
1. 点击 **"批量转换"** 标签页
2. 同时上传多个文档文件 (支持拖拽)
3. 查看文件信息确认支持情况
4. 点击 **"批量转换"** 按钮
5. 下载包含所有转换结果的ZIP文件

### 📊 界面功能说明

- **文件上传区域**: 支持拖拽上传，自动格式检测
- **转换状态显示**: 实时显示处理进度和结果
- **内容预览**: 即时查看转换后的Markdown内容
- **下载功能**: 单文件.md下载或批量ZIP打包
- **错误处理**: 详细的错误信息和处理建议

## ⚙️ 环境要求

- **Python**: 3.12 或更高版本
- **内存**: 建议 4GB 以上
- **磁盘空间**: 至少 2GB 可用空间
- **网络**: 首次安装需要联网下载依赖

## 🔧 高级配置

### 修改服务器配置

编辑 `app.py` 文件末尾的启动参数：

```python
demo.launch(
    server_name="0.0.0.0",  # 允许外部访问
    server_port=7860,       # 修改端口
    share=True,             # 创建公共访问链接
    auth=("user", "pass")   # 添加用户认证
)
```

### 性能优化建议

1. **大文件处理**: 建议单个文件不超过50MB
2. **批量处理**: 建议同时处理文件数不超过20个
3. **内存管理**: 定期重启服务以释放内存
4. **磁盘清理**: 临时文件会自动清理

## ❗ 注意事项

### 📝 文档转换质量

- **.docx文件**: 转换效果最佳，完美保持格式
- **.doc文件**: 可能存在兼容性问题，建议转换为.docx
- **复杂格式**: 表格、图片、公式等需要手动检查
- **中文支持**: 完全支持中文文档和文件名

### 🔒 安全说明

- 所有文件处理在本地进行，不会上传到外部服务器
- 临时文件会在处理完成后自动清理
- 建议在内网环境使用，避免暴露敏感文档

### 🐛 故障排除

#### 常见问题

1. **依赖安装失败**
   ```bash
   # 升级pip后重试
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

2. **端口占用**
   ```bash
   # 修改app.py中的server_port参数
   server_port=8080
   ```

3. **转换失败**
   - 检查文件格式是否支持
   - 确认文件没有损坏
   - 查看控制台错误日志

## 🛠️ 技术架构

- **后端框架**: Gradio 4.0+
- **转换引擎**: Microsoft MarkItDown 0.1.2
- **文档处理**: mammoth, openpyxl, python-pptx
- **AI识别**: magika, onnxruntime
- **界面风格**: 响应式设计，支持深色/浅色主题

## 📄 开源协议

本项目基于 MIT 协议开源，基于以下优秀项目：

- [Microsoft MarkItDown](https://github.com/microsoft/markitdown) - 核心转换引擎
- [Gradio](https://gradio.app/) - Web界面框架

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进这个项目！

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📞 支持

如果您在使用过程中遇到问题，请：

1. 查看 [常见问题](#-故障排除) 部分
2. 搜索已有的 [Issues](../../issues)
3. 创建新的 Issue 描述问题

---

⭐ 如果这个项目对您有帮助，请给个星标支持！ 
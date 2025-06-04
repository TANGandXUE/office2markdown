# MarkItDown 论文文档转换工具

这是一个基于Microsoft MarkItDown的文档转换工具集，用于将docx、doc等Office文档转换为Markdown格式，便于论文写作和参考资料整理。

## 环境要求

- Python 3.12+
- Conda 环境管理器

## 安装说明

### 1. 创建Conda环境
```bash
conda create -n markitdown python=3.12 -y
conda activate markitdown
```

### 2. 安装依赖
```bash
pip install markitdown
# 或者使用requirements.txt
pip install -r requirements.txt
```

## 支持的文件格式

- **Word文档**: `.docx`, `.doc`
- **PDF文档**: `.pdf`
- **PowerPoint**: `.pptx`
- **Excel表格**: `.xlsx`
- **网页文件**: `.html`, `.htm`

## 使用方法

### 单文件转换
```bash
python test_conversion.py "论文文档.docx" "输出文件.md"
```

### 批量转换当前目录所有文档
```bash
python batch_convert.py
```

### 转换指定文件
```bash
python batch_convert.py "文件1.docx" "文件2.doc" "文件3.pdf"
```

## 脚本说明

### test_conversion.py
- 单文件转换工具
- 支持预览转换结果
- 自动生成输出文件名

### batch_convert.py
- 批量转换工具
- 自动创建输出目录 `markdown_output`
- 显示转换进度和结果统计

## 输出结果

- 所有转换后的Markdown文件保存在 `markdown_output` 目录
- 保持原文件名，扩展名改为 `.md`
- 支持中文文件名

## 注意事项

1. **文件编码**: 输出的Markdown文件使用UTF-8编码
2. **复杂格式**: 表格、图片等复杂格式会尽力保持，但可能需要手动调整
3. **文件大小**: 大文件转换可能需要较长时间
4. **权限问题**: 确保对文件有读取权限

## 示例用法

```bash
# 激活环境
conda activate markitdown

# 转换单个文件
python test_conversion.py "上海海事大学学位论文与摘要的统一要求（修改版）.doc"

# 批量转换所有文档
python batch_convert.py

# 查看转换结果
ls markdown_output/
```

## 故障排除

### 如果遇到安装问题：
```bash
# 重新安装MarkItDown
pip uninstall markitdown
pip install markitdown

# 检查安装
python -c "import markitdown; print('安装成功')"
```

### 如果转换失败：
1. 检查文件是否存在且可读
2. 确保文件格式正确
3. 查看错误信息进行诊断

## 技术说明

本工具基于Microsoft的MarkItDown项目：
- GitHub: https://github.com/microsoft/markitdown
- 版本: 0.1.2
- 核心功能: 利用AI技术进行智能文档解析和转换 
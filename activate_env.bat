@echo off
echo 正在激活MarkItDown环境...
call conda activate markitdown
echo.
echo MarkItDown环境已激活！
echo.
echo 可用命令：
echo   python quick_start.py        - 交互式转换
echo   python batch_convert.py      - 批量转换所有文档
echo   python test_conversion.py    - 单文件转换工具
echo.
echo 示例：
echo   python test_conversion.py "文档.docx"
echo.
cmd /k 
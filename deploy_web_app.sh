#!/bin/bash

# 燃油追踪Web应用部署脚本

echo "正在部署燃油追踪Web应用..."

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python3"
    exit 1
fi

# 检查pip是否安装
if ! command -v pip3 &> /dev/null; then
    echo "错误: 未找到pip3，请先安装pip3"
    exit 1
fi

echo "安装依赖..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "依赖安装失败"
    exit 1
fi

echo "启动Web应用..."
echo "应用将在 http://0.0.0.0:5000 可访问"
echo "请在浏览器中打开此地址访问应用"
echo "按 Ctrl+C 停止应用"

# 启动Web应用
python3 fuel_tracker_web.py
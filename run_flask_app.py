#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
运行Flask版本的燃油追踪应用
"""

import subprocess
import sys
import os
import time
import socket
from threading import Thread


def check_port(port):
    """检查端口是否可用"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) != 0


def install_dependencies():
    """安装依赖"""
    print("正在检查依赖...")
    
    try:
        import flask
        import werkzeug
        print("✅ Flask 已安装")
        return True
    except ImportError:
        pass
    
    try:
        print("正在安装 Flask...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Flask 安装成功")
        return True
    except subprocess.CalledProcessError:
        print("❌ 安装失败，尝试单独安装 Flask")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "flask", "gunicorn"])
            print("✅ Flask 临时安装成功")
            return True
        except subprocess.CalledProcessError:
            print("❌ 无法安装 Flask，可能由于网络或SSL证书问题")
            return False


def run_app():
    """运行应用"""
    try:
        # 尝试导入 Flask
        try:
            from app import app
        except ImportError:
            print("❌ 找不到 app.py 文件")
            return
        
        port = 5000
        # 查找可用端口
        while not check_port(port) and port < 5020:
            port += 1
            
        if not check_port(port):
            print("❌ 没有可用端口")
            return
            
        print(f"🚀 启动燃油追踪应用...")
        print(f"🌐 访问地址: http://localhost:{port}")
        print("💡 提示: 按 Ctrl+C 停止应用")
        
        # 运行 Flask 应用
        app.run(host='0.0.0.0', port=port, debug=False)
        
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请先安装 Flask: pip install flask")
    except Exception as e:
        print(f"❌ 运行出错: {e}")


if __name__ == "__main__":
    print("🔧 燃油追踪应用启动器")
    print("="*40)
    
    # 检查是否有requirements.txt
    if os.path.exists("requirements.txt"):
        success = install_dependencies()
        if not success:
            print("\n⚠️  由于网络问题，将尝试使用系统自带的模块运行")
    
    run_app()
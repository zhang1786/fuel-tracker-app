#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
暴露本地应用到公网的简单方法
"""

import http.server
import socketserver
import threading
import time
import urllib.request
import json
from functools import partial


def get_local_ip():
    """获取本地IP地址"""
    import socket
    try:
        # 连接到一个远程地址以确定本地IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def check_port_open(port):
    """检查端口是否开放"""
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = s.connect_ex(('127.0.0.1', port))
    s.close()
    return result == 0


def main():
    print("🔍 检测本地环境...")
    
    # 检查我们的应用是否在运行
    if not check_port_open(8080):
        print("❌ 油耗追踪应用似乎没有在8080端口运行")
        print("💡 请先运行: python3 app.py")
        return
    
    local_ip = get_local_ip()
    print(f"🏠 本地IP地址: {local_ip}")
    print(f"🌐 您的应用正在运行: http://{local_ip}:8080")
    print(f"🔗 本地访问: http://127.0.0.1:8080 或 http://localhost:8080")
    print("\n💡 要让外部网络访问，请按照以下步骤操作：")
    print("1. 配置路由器端口转发，将外部端口映射到本地8080端口")
    print("2. 或者使用SSH隧道: ssh -R 80:localhost:8080 serveo.net")
    print("3. 或者使用Cloudflare Tunnel或其他隧道服务")
    print("\n注意：直接暴露应用可能存在安全风险，请谨慎操作。")


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
更新服务器上的燃油追踪应用
此脚本将从GitHub拉取最新代码并重启服务
"""

import paramiko
import sys
import os
from pathlib import Path

def update_server_app():
    """
    更新服务器上的应用
    """
    hostname = '8.137.39.61'
    username = 'admin'
    key_filename = os.path.expanduser('~/.ssh/github_key')  # 使用本地SSH密钥
    
    # 创建SSH客户端
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # 连接到服务器
        print(f"正在连接到 {hostname}...")
        ssh.connect(hostname, username=username, key_filename=key_filename)
        
        print("连接成功！正在更新应用...")
        
        # 执行更新命令
        commands = [
            "cd /home/admin/fuel-tracker-app",
            "git pull origin main",  # 拉取最新代码
            "pkill -f gunicorn || true",  # 停止现有gunicorn进程
            "sleep 3",  # 等待进程结束
            "/home/admin/.local/bin/gunicorn -w 1 -b 0.0.0.0:8000 app:app &",  # 重启服务
        ]
        
        full_command = " && ".join(commands)
        print(f"执行命令: {full_command}")
        
        stdin, stdout, stderr = ssh.exec_command(full_command)
        
        # 获取输出
        stdout_result = stdout.read().decode('utf-8')
        stderr_result = stderr.read().decode('utf-8')
        
        print("标准输出:")
        print(stdout_result)
        
        if stderr_result:
            print("错误输出:")
            print(stderr_result)
        
        print("应用已更新并重启！")
        
    except Exception as e:
        print(f"更新过程中出现错误: {str(e)}")
        return False
        
    finally:
        ssh.close()
    
    return True

if __name__ == "__main__":
    update_server_app()
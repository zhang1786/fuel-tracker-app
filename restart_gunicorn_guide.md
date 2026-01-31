# 重启Gunicorn服务的方法

## 方法一：停止和启动Gunicorn（推荐）

### 1. 查看正在运行的Gunicorn进程
```bash
ps aux | grep gunicorn
```

### 2. 停止Gunicorn服务
```bash
pkill -f gunicorn
```

或者，如果您知道具体的PID（进程ID）：
```bash
kill -TERM <PID>
```

### 3. 启动Gunicorn服务
```bash
cd /home/admin/fuel-tracker-app
/home/admin/.local/bin/gunicorn -w 1 -b 0.0.0.0:8000 app:app &
```

## 方法二：优雅重启Gunicorn

### 1. 发送HUP信号进行优雅重启
```bash
pkill -HUP gunicorn
```

## 方法三：使用完整命令序列

```bash
# 进入应用目录
cd /home/admin/fuel-tracker-app

# 停止所有gunicorn进程
pkill -f gunicorn

# 等待几秒确保进程完全停止
sleep 3

# 启动新的gunicorn进程
/home/admin/.local/bin/gunicorn -w 1 -b 0.0.0.0:8000 app:app &

# 检查进程是否启动成功
ps aux | grep gunicorn
```

## 验证服务是否运行

### 检查Gunicorn进程
```bash
ps aux | grep gunicorn
```

### 检查端口占用
```bash
netstat -tlnp | grep :8000
```

或者使用ss命令：
```bash
ss -tlnp | grep :8000
```

### 测试服务
```bash
curl http://localhost:8000
```

## 注意事项

- 确保在正确的应用目录中运行Gunicorn
- 确保使用的Python环境中有Gunicorn
- 使用`&`符号在后台运行Gunicorn
- 检查防火墙设置确保端口8000对外可用
- 如果使用systemctl管理服务，可能需要使用systemctl命令重启
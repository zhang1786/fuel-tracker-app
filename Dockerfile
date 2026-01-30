# 使用官方Python运行时作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制requirements文件（如果有的话）
COPY requirements.txt .

# 安装Flask和其他依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码到容器中
COPY . .

# 暴露端口5000
EXPOSE 5000

# 运行应用
CMD ["python", "app.py"]
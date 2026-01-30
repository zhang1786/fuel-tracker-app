# 燃油追踪应用 - 部署指南

## 部署选项

### 选项1：Render.com（推荐新手）
1. 注册 [Render](https://render.com) 账号
2. Fork 这个仓库或上传代码
3. 创建一个新的 Web Service
4. 选择 Docker 部署或直接部署 Python 应用
5. 使用以下配置：
   - Runtime: Python 3
   - Start Command: `gunicorn app:app`

### 选项2：Railway.app
1. 注册 [Railway](https://railway.app) 账号
2. 点击 "New Project"
3. 选择 "Deploy from GitHub"
4. 选择您的仓库
5. Railway 会自动检测并部署

### 选项3：Heroku
1. 注册 [Heroku](https://heroku.com) 账号
2. 安装 Heroku CLI
3. 创建新的应用
4. 推送代码

### 选项4：Vercel（通过 Docker）
1. 注册 [Vercel](https://vercel.com) 账号
2. 使用 Vercel CLI 部署

## 文件清单

您需要以下文件来部署：

- `app.py` - 主应用文件
- `requirements.txt` - 依赖文件
- `Procfile` - 进程文件
- `runtime.txt` - Python 版本指定

## 依赖文件

### requirements.txt
```
Flask==2.3.3
gunicorn==21.2.0
Werkzeug==2.3.7
```

### Procfile
```
web: gunicorn app:app
```

### runtime.txt
```
python-3.11
```

## 部署到 Render 的详细步骤

1. 准备代码文件：
   - app.py (已提供)
   - requirements.txt (见上方)
   - Procfile (见上方)
   - runtime.txt (见上方)

2. 在 Render 控制面板点击 "New +" 按钮

3. 选择 "Web Service"

4. 连接您的 GitHub/GitLab 账户并选择包含这些文件的仓库

5. Render 会自动检测到 Python 应用并使用提供的配置

6. 点击 "Create Web Service"

7. 等待构建完成，完成后您会获得一个公共 URL

## 本地测试部署

如果您想在本地测试部署配置：

```bash
# 安装依赖
pip install Flask gunicorn

# 测试运行
gunicorn app:app

# 或者直接用 Flask 运行
python app.py
```

## 数据持久化注意

**重要提醒：** 免费的云平台通常不保留文件系统上的数据。为了长期保存数据，您应该：

1. 定期备份 `fuel_records_simple.json` 文件
2. 考虑使用数据库（如 SQLite with persistent storage 或 PostgreSQL）
3. 将数据导出到外部存储

## 自定义域名

部署完成后，您可以绑定自定义域名：
1. 在域名提供商处设置 CNAME 记录指向部署平台
2. 在部署平台的设置中添加自定义域名

## SSL 证书

大多数现代云平台会自动提供 HTTPS 支持，无需额外配置。

## 故障排除

如果遇到问题：
1. 检查日志输出
2. 确保所有必需文件都已上传
3. 验证端口使用环境变量 `$PORT`
4. 确保应用绑定到 `0.0.0.0` 而不是 `localhost`

## 安全建议

- 限制对应用的访问（如果平台支持）
- 定期备份数据
- 监控应用性能和用量
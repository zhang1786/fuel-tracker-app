# 燃油追踪应用 - Render.com 部署指南

## 第一步：准备代码

所有必需的文件已在当前目录中：
- `app.py` - 主应用文件
- `requirements.txt` - 依赖文件
- `Procfile` - 启动配置
- `runtime.txt` - Python版本指定

## 第二步：创建 Render 账户

1. 访问 [https://render.com](https://render.com)
2. 点击 "Sign Up" 并使用邮箱或GitHub账户注册
3. 验证邮箱（如果需要）

## 第三步：连接 GitHub 仓库

### 方法A：Fork现有仓库（最快）
1. 在GitHub上fork这个仓库（包含fuel-tracker-deployment目录中的所有文件）
2. 登录Render控制台
3. 点击 "New +" 按钮 → "Web Service"
4. 点击 "Connect Account" 连接您的GitHub账户
5. 选择您刚fork的仓库

### 方法B：手动上传文件
1. 创建一个新的GitHub仓库
2. 将以上四个文件上传到仓库
3. 按照方法A的后续步骤操作

## 第四步：配置部署

在 Render 控制台中，您会看到以下配置选项：

### 必填项：
- **Repository**: 选择您连接的仓库
- **Branch**: 选择 main 或 master 分支
- **Runtime**: Render 会自动检测为 Python
- **Build Command**: Render 会自动检测（pip install -r requirements.txt）
- **Start Command**: Render 会自动检测（gunicorn app:app）

### 环境设置：
- **Region**: 选择 closest 或 Frankfurt (欧洲，对亚洲访问较友好)
- **Instance Type**: Free (免费计划，足够使用)

## 第五步：部署应用

1. 点击 "Create Web Service" 按钮
2. Render 会开始构建您的应用，这可能需要几分钟
3. 构建过程中，您可以在控制台看到实时日志
4. 构建成功后，您会看到分配的URL（格式为：https://xxxx.onrender.com）

## 第六步：访问您的应用

1. 点击分配的URL或在新标签页中打开
2. 您的燃油追踪应用现在可以从任何地方访问了！

## 第七步：（可选）自定义域名

如果您有自己的域名：
1. 在域名提供商处添加 CNAME 记录
2. 记录值设为：`cname.render.com`
3. 在 Render 控制台的 "Domains" 标签页中添加您的自定义域名

## 数据备份提醒

**重要**：免费账户不会永久保存文件系统数据。为防止数据丢失，请定期：
1. 导出数据（目前应用尚未实现导出功能，但会保存在服务器上）
2. 我们将在后续版本中添加数据导出功能

## 常见问题

### Q: 部署后无法访问？
A: 检查：
- 是否正确设置了 Procfile
- 端口是否使用环境变量 $PORT
- 应用是否绑定到 0.0.0.0 而非 localhost

### Q: 数据是否会丢失？
A: 免费计划可能会重置存储。建议定期记录重要数据。

### Q: 如何更新应用？
A: 修改代码并推送到 GitHub，Render 会自动重新部署（如果启用了自动部署）。

## 完成！

现在您的燃油追踪应用已部署到云端，可以从任何地方访问。分享生成的URL给需要的人即可。
# 燃油追踪应用

一个简单易用的燃油消耗追踪Web应用，帮助您记录和分析车辆的燃油效率。

## 功能特性

- 📊 **仪表盘** - 显示关键统计信息
- ➕ **添加记录** - 输入加油日期、里程、加油量、油价等信息
- 📋 **查看记录** - 显示所有加油记录
- 📊 **油耗详情** - 计算并显示油耗数据（L/100km）
- 📈 **统计信息** - 总花费、平均油耗等汇总数据

## 部署说明

### 云端部署（推荐）

按照 `RENDER_DEPLOYMENT_STEPS.md` 中的说明将应用部署到 Render.com：

1. 访问 [Render.com](https://render.com) 并创建账户
2. 连接您的 GitHub 账户
3. 选择包含此代码的仓库
4. Render 会自动构建并部署应用
5. 获取公共 URL 并开始使用

### 本地运行

如果您想在本地运行：

```bash
# 安装依赖
pip install -r requirements.txt

# 运行应用
python app.py
```

然后在浏览器中访问 `http://localhost:5000`

## 技术栈

- Python Flask
- HTML/CSS/JavaScript
- JSON 数据存储

## 数据持久性

**注意**：在免费云服务上，数据可能不会永久保存。建议定期备份您的燃油记录。

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目！
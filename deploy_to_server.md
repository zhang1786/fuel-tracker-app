# 部署更新到服务器

GitHub仓库已成功更新，现在需要将更改部署到服务器。

## 步骤

1. 登录到服务器：
   ```bash
   ssh admin@8.137.39.61
   ```

2. 进入应用目录：
   ```bash
   cd /home/admin/fuel-tracker-app
   ```

3. 拉取最新代码：
   ```bash
   git pull origin main
   ```

4. 重启Gunicorn服务：
   ```bash
   pkill -f gunicorn
   /home/admin/.local/bin/gunicorn -w 1 -b 0.0.0.0:8000 app:app &
   ```

## 验证

访问 http://8.137.39.61 确认删除功能已正常工作。

## 功能说明

本次更新添加了燃油追踪应用的删除功能：
- 用户可以在记录表格中看到删除按钮
- 点击删除按钮会弹出确认对话框
- 确认后会通过API删除对应记录
- 删除后页面会自动刷新
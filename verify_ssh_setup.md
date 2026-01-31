# GitHub SSH 密钥验证和设置指南

## 步骤 1: 验证本地 SSH 密钥

您的本地 SSH 密钥已生成，指纹为：
SHA256:5ClHMKdvtAvHHwmdbLM7KjB5Z0UTYVbYWNFUmKSptkA

## 步骤 2: 检查 GitHub 上的 SSH 密钥

请按以下步骤检查 SSH 密钥是否已正确添加到 GitHub：

1. 登录到 GitHub 网站
2. 点击右上角的头像，选择 "Settings"
3. 在左侧菜单中选择 "SSH and GPG keys"
4. 查找名为 "Clawd SSH Key" 或类似名称的密钥
5. 确认该密钥的内容与下面的完全一致：

```
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDTHPBItXqfJ51Z7GhscAJm9ng3rOKCiWDkroR9agr0EVnjtXJ+RxlADSwycCx32ph0wad0MpR42Mkp901qBwQoYXDhKAL5qR0mimHjwoHeAA48GQWY00Rg9vDRDHbnqDVeKQ40SBHeKCIidjx6dUNE5wkLMW+r5J34LpQh9k+Zsqt+EHXUQtlIVs7mBb8PlEuJ2VmjnZ8KsLr6sEQP/qFXYIAcub3TMVAJXcKi7ACqp0rW4LOWF6UXkj3M6TFWHjycYSxaJwl/A+76YHQpdL+PF2ScduQ9qD5s/v1NqL8c9tuATLQkLgsi0XOGb4x2NCil1xtY28MKsGI9NyiDkYuzkTzDQAp6PM6sECSQX6EmTUzD3maWvHbLR7/aXY0d/KMu+a/DF9LqPgdWFoE8LbLx2h1wyll/XtnOU7Sc5GZUfSY9La5o2Djg+lO7iI3vWOEVaH35zjckRZ+K1IbmRMHdhqINLYB5teLVshwQCVK2mu86FPTc+7heAba7AOlHTyQ9zKzUSZ8jHgtQP04fnht4mKjQrJ8mPR1/xJz7mlV46DhrkRE3blpieOO0N78148uDM3rXeIVx3XFvvjFgmRq9Jk7TpvJY0SrvnUf7YEkPy/9d81MlCg5lKniNQROYVlv3J5ziGsuZGnodBHRdNZPSvXGUtapqzWlp+Ej6y5/JMQ== zhang1786@users.noreply.github.com
```

## 步骤 3: 如果密钥未正确添加，请重新添加

如果在 GitHub 上找不到该密钥，或密钥内容不匹配，请按以下步骤重新添加：

1. 在 GitHub Settings 的 "SSH and GPG keys" 页面点击 "New SSH key"
2. 标题填入 "Clawd SSH Key"
3. 类型选择 "Authentication Key" 或 "SSH"
4. 将上面的密钥内容完整粘贴到 "Key" 字段
5. 点击 "Add SSH key"

## 步骤 4: 测试连接

添加完成后，等待几分钟让设置生效，然后在终端中运行：
ssh -T git@github.com

## 步骤 5: 如果仍有问题

如果仍然无法连接，请尝试以下步骤：

1. 清除 SSH 缓存：
   ssh-add -D
   ssh-add ~/.ssh/github_key

2. 重新设置远程仓库：
   git remote set-url origin git@github.com:zhang1786/fuel-tracker-app.git

3. 尝试推送：
   git push origin main
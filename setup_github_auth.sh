#!/bin/bash

echo "设置GitHub认证..."

# 检查SSH密钥是否存在
if [ ! -f ~/.ssh/github_key ]; then
    echo "创建SSH密钥..."
    ssh-keygen -t rsa -b 4096 -C "zhang1786@users.noreply.github.com" -f ~/.ssh/github_key -N ""
fi

# 启动ssh-agent并添加密钥
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/github_key

echo "SSH公钥内容如下："
echo ""
cat ~/.ssh/github_key.pub
echo ""
echo ""
echo "请执行以下步骤："
echo "1. 复制上面的公钥内容"
echo "2. 访问 https://github.com/settings/ssh/new"
echo "3. 粘贴公钥内容并添加标题 'Clawd SSH Key'"
echo "4. 点击 'Add SSH key' 按钮"
echo ""
echo "完成上述步骤后，运行以下命令来测试连接："
echo "ssh -T git@github.com"
echo ""
echo "然后设置远程仓库为SSH方式："
echo "git remote set-url origin git@github.com:zhang1786/fuel-tracker-app.git"
echo ""
echo "最后推送更改："
echo "git push origin main"
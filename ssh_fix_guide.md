# SSH认证修复指南

## 问题诊断

当前SSH认证失败的原因可能是：
1. 服务器的主机密钥未正确添加到本地known_hosts
2. 本地SSH密钥未正确配置到远程服务器
3. SSH密钥权限设置不当

## 解决步骤

### 1. 确保本地SSH密钥配置正确

```bash
# 检查本地SSH密钥
ls -la ~/.ssh/

# 确保SSH代理运行
eval "$(ssh-agent -s)"

# 添加SSH密钥到代理
ssh-add ~/.ssh/github_key
```

### 2. 配置服务器的主机密钥

```bash
# 添加服务器主机密钥到known_hosts
ssh-keyscan -H 8.137.39.61 >> ~/.ssh/known_hosts
```

### 3. 配置服务器的authorized_keys

由于我们无法直接通过SSH登录，需要通过其他方式将本地公钥添加到服务器：

```bash
# 查看本地公钥内容
cat ~/.ssh/github_key.pub
```

然后将公钥内容添加到服务器的 `~/.ssh/authorized_keys` 文件中。

### 4. 创建SSH配置文件

```bash
# 编辑SSH配置
nano ~/.ssh/config
```

添加以下内容：
```
Host myserver
    HostName 8.137.39.61
    User admin
    IdentityFile ~/.ssh/github_key
    IdentitiesOnly yes
```

### 5. 测试连接

```bash
# 使用配置的主机名连接
ssh myserver
```

## 替代方案

如果上述方法仍无法解决问题，可以考虑：

1. 使用服务器提供商的控制台访问功能
2. 通过API或控制面板修改服务器配置
3. 重新生成SSH密钥对并配置到服务器
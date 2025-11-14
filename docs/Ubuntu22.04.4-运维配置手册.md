# Ubuntu 22.04.4 常用配置和运维手册

<div align="center">

![Ubuntu Logo](https://img.shields.io/badge/Ubuntu-22.04.4-orange.svg)
![Linux](https://img.shields.io/badge/Linux-Expert-blue.svg)
![DevOps](https://img.shields.io/badge/DevOps-Configuration-green.svg)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success.svg)

**🐧 面向Linux技术初学者的Ubuntu运维配置手册**<br/>

[🚀 基础配置](#-基础配置) • [🔧 系统优化](#-系统优化) • [🛠️ 开发环境](#️-开发环境) • [📊 监控运维](#-监控运维)

</div>

---

## 📋 目录

- [1. 远程连接工具配置](#1-远程连接工具配置)
- [2. 网络配置](#2-网络配置)
- [3. 用户权限管理](#3-用户权限管理)
- [4. 系统时间同步](#4-系统时间同步)
- [5. 命令行优化](#5-命令行优化)
- [6. 磁盘管理](#6-磁盘管理)
- [7. DNS配置](#7-dns配置)
- [8. Git环境配置](#8-git环境配置)
- [9. 网络代理配置](#9-网络代理配置)
- [10. 容器化环境](#10-容器化环境)
- [11. Node.js开发环境](#11-nodejs开发环境)
- [12. 系统监控与维护](#12-系统监控与维护)

---

## 🎯 手册特色

- **🔰 零基础友好**：从最基础的概念开始，逐步深入
- **📝 详细步骤**：每个配置都有详细的操作步骤和命令
- **⚠️ 安全提示**：重要操作前都有安全提醒和备份建议
- **🛡️ 最佳实践**：遵循Linux系统管理的最佳实践
- **🔧 实战导向**：所有配置都经过实际环境验证

### 🚀 快速开始

本手册提供了两个实用脚本帮助你快速配置和检查Ubuntu系统：

#### 📦 快速配置脚本
```bash
# 下载快速配置脚本
wget https://raw.githubusercontent.com/your-repo/Agent-101/main/scripts/ubuntu-quick-setup.sh
chmod +x ubuntu-quick-setup.sh

# 交互式配置
./ubuntu-quick-setup.sh

# 一键完整安装
./ubuntu-quick-setup.sh --full
```

#### 🔍 系统检查脚本
```bash
# 下载系统检查脚本
wget https://raw.githubusercontent.com/your-repo/Agent-101/main/scripts/system-check.sh
chmod +x system-check.sh

# 运行系统检查
./system-check.sh
```

---

## 1. 远程连接工具配置

### 1.1 SSH工具推荐

为了方便管理Ubuntu服务器，推荐使用专业的SSH客户端工具：

#### Xshell 和 Xftp (Windows用户推荐)

**下载地址**: https://www.xshell.com/zh/free-for-home-school/

**特点**:
- Xshell: 功能强大的SSH终端客户端
- Xftp: 图形化的文件传输工具
- 支持多标签页管理
- 免费版本供个人和学校使用

#### 其他推荐工具

- **Windows**: PuTTY, MobaXterm, Windows Terminal + OpenSSH
- **macOS**: Terminal (内置), iTerm2
- **Linux**: 终端 (内置)

### 1.2 SSH服务配置

确保Ubuntu系统已安装并启动SSH服务：

```bash
# 安装SSH服务
sudo apt update
sudo apt install openssh-server

# 启动SSH服务
sudo systemctl start ssh
sudo systemctl enable ssh

# 检查SSH服务状态
sudo systemctl status ssh
```

---

## 2. 网络配置

### 2.1 配置静态IP地址

Ubuntu 22.04 使用 Netplan 来管理网络配置。

#### 2.1.1 查看网络接口

```bash
# 查看所有网络接口
ip a

# 查看路由信息
ip route
```

#### 2.1.2 配置静态IP

1. **进入Netplan配置目录**:
   ```bash
   cd /etc/netplan/
   ls -la
   ```

2. **备份现有配置**:
   ```bash
   sudo cp 00-installer-config.yaml 00-installer-config.yaml.bak
   ```

3. **编辑配置文件**:
   ```bash
   sudo nano 00-installer-config.yaml
   ```

4. **静态IP配置示例**:
   ```yaml
   network:
     version: 2
     renderer: networkd
     ethernets:
       ens33:  # 替换为你的实际网络接口名
         dhcp4: no
         dhcp6: no
         addresses:
           - 192.168.1.100/24  # 你的静态IP地址/子网掩码
         routes:
           - to: default
             via: 192.168.1.1   # 你的网关地址
         nameservers:
           addresses: [8.8.8.8, 1.1.1.1]  # DNS服务器
   ```

5. **应用配置**:
   ```bash
   sudo netplan apply
   ```

6. **验证配置**:
   ```bash
   ip a show ens33
   ping 8.8.8.8
   ```

#### 2.1.3 配置说明

- `addresses`: 静态IP地址，使用CIDR格式 (/24 = 255.255.255.0)
- `routes`: 路由配置，to: default 表示默认路由
- `nameservers`: DNS服务器配置

⚠️ **注意事项**:
- YAML文件对缩进非常敏感，请使用空格而不是Tab
- 配置错误可能导致网络中断，建议在本地操作或准备好恢复方案

---

## 3. 用户权限管理

### 3.1 开启root用户登录

#### 3.1.1 设置root密码

```bash
sudo passwd root
```

输入新密码并确认：
```
New password: 
Retype new password: 
passwd: password updated successfully
```

#### 3.1.2 允许SSH登录

1. **编辑SSH配置文件**:
   ```bash
   sudo vim /etc/ssh/sshd_config
   ```

2. **修改配置项**:
   ```bash
   # 找到以下行并修改为：
   PermitRootLogin yes
   ```

3. **重启SSH服务**:
   ```bash
   sudo systemctl restart ssh
   ```

#### 3.1.3 安全建议

⚠️ **安全警告**: 
- 开启root登录存在安全风险
- 建议仅在必要时开启
- 生产环境建议使用sudo用户而非直接使用root
- 考虑使用密钥认证替代密码认证

---

## 4. 系统时间同步

### 4.1 配置时区

设置为北京时间（中国标准时间 UTC+8）：

```bash
# 设置时区
sudo timedatectl set-timezone Asia/Shanghai

# 查看时间状态
timedatectl status
```

### 4.2 安装时间同步服务

#### 4.2.1 使用Chrony（推荐）

```bash
# 安装chrony
sudo apt update
sudo apt install chrony

# 配置时间服务器
sudo vim /etc/chrony/chrony.conf
```

添加国内时间服务器：
```bash
# 阿里云NTP服务器
server ntp.aliyun.com iburst
server ntp1.aliyun.com iburst
server ntp2.aliyun.com iburst
```

#### 4.2.2 启动并启用服务

```bash
# 重启chrony服务
sudo systemctl restart chronyd
sudo systemctl enable chronyd

# 立即同步时间
sudo chronyc -a makestep

# 查看同步状态
chronyc tracking
```

#### 4.2.3 使用NTP（备选方案）

```bash
# 安装ntp
sudo apt install ntp

# 配置NTP服务器
sudo vim /etc/ntp.conf
```

添加配置：
```bash
server ntp.aliyun.com
server ntp1.aliyun.com
server ntp2.aliyun.com
```

启动服务：
```bash
sudo systemctl restart ntp
sudo systemctl enable ntp
```

---

## 5. 命令行优化

### 5.1 启用Bash自动补全

Ubuntu 22.04 默认已启用，如果不工作可以手动配置：

#### 5.1.1 安装bash-completion

```bash
sudo apt update
sudo apt install bash-completion
```

#### 5.1.2 配置bash-completion

编辑 `~/.bashrc` 文件：
```bash
vim ~/.bashrc
```

确保包含以下内容：
```bash
if [ -f /etc/bash_completion ] && ! shopt -oq posix; then
    . /etc/bash_completion
fi
```

#### 5.1.3 应用配置

```bash
source ~/.bashrc
```

#### 5.1.4 验证功能

```bash
# 测试自动补全
type _completion_loader
```

### 5.2 命令行美化（可选）

#### 5.2.1 安装Oh My Bash

```bash
# 安装Oh My Bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/ohmybash/oh-my-bash/master/tools/install.sh)"
```

#### 5.2.2 配置主题

编辑 `~/.bashrc`：
```bash
# 修改主题
OSH_THEME="powerline"
```

---

## 6. 磁盘管理

### 6.1 查看磁盘使用情况

```bash
# 查看磁盘使用情况
df -Th

# 查看磁盘分区
fdisk -l

# 查看LVM信息
sudo vgdisplay
sudo lvdisplay
```

### 6.2 根分区扩容

#### 6.2.1 扩展LVM逻辑卷

假设系统使用LVM管理磁盘：

```bash
# 查看卷组信息
sudo vgdisplay

# 如果有可用空间，直接扩展逻辑卷
sudo lvextend -L +50G /dev/mapper/ubuntu--vg-ubuntu--lv

# 扩展文件系统
sudo resize2fs /dev/mapper/ubuntu--vg-ubuntu--lv
```

#### 6.2.2 添加新磁盘到卷组

如果需要添加新磁盘：

```bash
# 创建新分区（使用fdisk）
sudo fdisk /dev/sdb

# 创建物理卷
sudo pvcreate /dev/sdb1

# 扩展卷组
sudo vgextend ubuntu-vg /dev/sdb1

# 扩展逻辑卷（使用所有可用空间）
sudo lvextend -l +100%FREE /dev/mapper/ubuntu--vg-ubuntu--lv

# 扩展文件系统
sudo resize2fs /dev/mapper/ubuntu--vg-ubuntu--lv
```

#### 6.2.3 验证扩容结果

```bash
df -Th
```

⚠️ **安全提示**: 
- 磁盘操作有数据丢失风险，请务必备份重要数据
- 在生产环境操作前，建议在测试环境验证

#### 6.2.4 Ubuntu 根目录 LVM 扩容详细操作步骤

没问题，这是一份完整的操作步骤，用于在 Ubuntu 22.04 系统中，将已有的 **Logical Volume Management (LVM)** 根目录 (`/`) 空间从大约 58 GiB 扩容到大约 146 GiB，利用了未分配的磁盘空间。

**目标:** 将根目录挂载点 `/` 所在的逻辑卷 `/dev/mapper/ubuntu--vg-ubuntu--lv` 从约 58 GiB 扩容到约 146 GiB，使用 `/dev/sda` 上的剩余空间。

##### 1. 检查当前磁盘和文件系统状态

首先，确认根目录的文件系统大小和磁盘分区情况。

| 命令       | 目的                         | 初始结果分析                                                 |
| ---------- | ---------------------------- | ------------------------------------------------------------ |
| `df -Th`   | 查看文件系统挂载点使用情况。 | 根目录 `/` 初始大小为 **57G**，挂载在 `/dev/mapper/ubuntu--vg-ubuntu--lv`。 |
| `fdisk -l` | 列出所有磁盘和分区信息。     | 确认主要磁盘是 `/dev/sda`，总大小 **150 GiB**。现有分区 `/dev/sda3` 只有 **58G**，说明磁盘上有大量未分配空间。 |

------

##### 2. 创建新的磁盘分区

使用 `fdisk` 工具在 `/dev/sda` 磁盘上创建一个新的分区，以利用剩余空间。

Bash

```Bash
fdisk /dev/sda
```

在 `fdisk` 提示符下执行以下步骤：

1. 输入 `n` **(new)** 创建新分区。
2. **Partition number (4-128, default 4):** 直接按 **Enter** 键接受默认的下一个分区号（例如 `4`）。
3. **First sector (...):** 直接按 **Enter** 键接受默认值，从剩余空间的起始扇区开始。
4. **Last sector, +/-sectors or +/-size{K,M,G,T,P} (...):** 直接按 **Enter** 键接受默认值，使用所有剩余空间（这里创建了一个 **90 GiB** 的新分区 `/dev/sda4`）。
5. 输入 `p` **(print)** 检查新的分区表，确认 `/dev/sda4` 已创建。
6. 输入 `w` **(write)** 将更改写入磁盘并退出 `fdisk`。

##### 3. 通知内核分区表变更

为了让操作系统立即识别新的分区 `/dev/sda4`，需要运行 `partprobe`。

```Bash
partprobe
```

##### 4. 将新分区添加到 LVM (Logical Volume Management)

现在，将新创建的分区 `/dev/sda4` 添加到 LVM 体系中。

###### 4.1. 创建物理卷 (PV)

将 `/dev/sda4` 初始化为一个 **Physical Volume (PV)**。

```Bash
pvcreate /dev/sda4
```

###### 4.2. 扩展卷组 (VG)

将新的物理卷 `/dev/sda4` 添加到包含根逻辑卷的卷组 **ubuntu-vg** 中。

```Bash
vgextend ubuntu-vg /dev/sda4
```

##### 5. 扩展逻辑卷和文件系统

现在卷组已经拥有了额外的空间，可以扩展逻辑卷和其上的文件系统了。

###### 5.1. 扩展逻辑卷 (LV)

使用卷组中 **100% 的空闲空间** (`+100%FREE`) 来扩展根目录逻辑卷 `/dev/mapper/ubuntu--vg-ubuntu--lv`。

```Bash
lvextend -l +100%FREE /dev/mapper/ubuntu--vg-ubuntu--lv
```

###### 5.2. 调整文件系统大小

最后，调整逻辑卷上的 **ext4 文件系统**大小，以使用逻辑卷的全部新空间。因为文件系统处于挂载状态 (`on-line resizing required`)，`resize2fs` 会自动在线完成扩容。

```Bash
resize2fs /dev/mapper/ubuntu--vg-ubuntu--lv
```

##### 6. 验证扩容结果

运行 `df -Th` 确认根目录 `/` 的大小是否已成功增加。

```Bash
df -Th /
```

###### **扩容后结果:**

```Bash
Filesystem                                Type  Size Used Avail Use% Mounted on
/dev/mapper/ubuntu--vg-ubuntu--lv ext4  146G  18G 122G  13% /
```

✅ 根目录的文件系统大小已成功从 **57G** 扩容到 **146G**。

---

## 7. DNS配置

### 7.1 永久修改DNS

#### 7.1.1 使用systemd-resolved

编辑配置文件：
```bash
sudo vim /etc/systemd/resolved.conf
```

配置DNS服务器：
```bash
[Resolve]
DNS=8.8.8.8 114.114.114.114
FallbackDNS=1.1.1.1
Domains=
LLMNR=yes
MulticastDNS=yes
DNSSEC=yes
Cache=no-negative
```

#### 7.1.2 重启服务

```bash
# 重启systemd-resolved服务
sudo systemctl restart systemd-resolved
sudo systemctl enable systemd-resolved

# 备份并重新链接resolv.conf
sudo mv /etc/resolv.conf /etc/resolv.conf.bak
sudo ln -s /run/systemd/resolve/resolv.conf /etc/resolv.conf
```

### 7.2 临时修改DNS

```bash
# 临时修改DNS
sudo vim /etc/resolv.conf
```

添加DNS服务器：
```bash
nameserver 8.8.8.8
nameserver 114.114.114.114
```

### 7.3 DNS服务器推荐

| 服务商 | 主DNS | 备DNS | 特点 |
|--------|-------|-------|------|
| Google | 8.8.8.8 | 8.8.4.4 | 全球通用，响应快 |
| Cloudflare | 1.1.1.1 | 1.0.0.1 | 注重隐私，速度快 |
| 114DNS | 114.114.114.114 | 114.114.115.115 | 国内优化 |
| 阿里DNS | 223.5.5.5 | 223.6.6.6 | 国内服务商 |

---

## 8. Git环境配置

### 8.1 配置Git用户信息

```bash
# 配置全局用户名和邮箱
git config --global user.name "你的用户名"
git config --global user.email "你的邮箱地址"

# 示例
git config --global user.name "FlyAIBox"
git config --global user.email "fly910905@sina.com"

# 查看配置
git config --global user.name
git config --global user.email
```

### 8.2 生成SSH密钥

#### 8.2.1 检查现有密钥

```bash
ls -al ~/.ssh
```

#### 8.2.2 生成新密钥

推荐使用Ed25519算法：
```bash
ssh-keygen -t ed25519 -C "你的邮箱地址"
```

如果系统不支持Ed25519，使用RSA：
```bash
ssh-keygen -t rsa -b 4096 -C "你的邮箱地址"
```

#### 8.2.3 添加密钥到SSH代理

```bash
# 启动ssh-agent
eval "$(ssh-agent -s)"

# 添加私钥
ssh-add ~/.ssh/id_ed25519
```

#### 8.2.4 复制公钥

```bash
# 安装xclip用于复制
sudo apt install xclip

# 复制公钥到剪贴板
cat ~/.ssh/id_ed25519.pub | xclip -selection clipboard

# 或者直接查看公钥内容
cat ~/.ssh/id_ed25519.pub
```

### 8.3 添加公钥到Git服务

#### GitHub
1. 登录GitHub → Settings → SSH and GPG keys
2. 点击 "New SSH key"
3. 粘贴公钥内容并保存

#### GitLab
1. 登录GitLab → User Settings → SSH Keys
2. 粘贴公钥内容并保存

#### Gitee（码云）
1. 登录Gitee → 设置 → SSH公钥
2. 粘贴公钥内容并保存

### 8.4 测试SSH连接

```bash
# 测试GitHub连接
ssh -T git@github.com

# 测试GitLab连接
ssh -T git@gitlab.com

# 测试Gitee连接
ssh -T git@gitee.com
```

### 8.5 删除Git配置（可选）

如需重新配置：
```bash
# 删除全局用户配置
git config --global --unset user.name
git config --global --unset user.email

# 删除SSH密钥
rm ~/.ssh/id_ed25519
rm ~/.ssh/id_ed25519.pub
```

---

## 9. 网络代理配置

### 9.1 安装v2rayA

#### 9.1.1 添加软件源

```bash
# 添加公钥
wget -qO - https://apt.v2raya.org/key/public-key.asc | sudo tee /etc/apt/keyrings/v2raya.asc

# 添加软件源
echo "deb [signed-by=/etc/apt/keyrings/v2raya.asc] https://apt.v2raya.org/ v2raya main" | sudo tee /etc/apt/sources.list.d/v2raya.list

# 更新软件包列表
sudo apt update
```

#### 9.1.2 安装v2rayA

```bash
# 安装v2rayA和v2ray内核
sudo apt install v2raya v2ray
```

#### 9.1.3 启动服务

```bash
# 启动v2rayA
sudo systemctl start v2raya.service

# 设置开机自启
sudo systemctl enable v2raya.service

# 检查服务状态
sudo systemctl status v2raya.service
```

### 9.2 配置v2rayA

1. **访问Web界面**: http://192.168.172.128:2017
2. **创建管理员账号**: 首次访问需要创建账号
3. **导入节点**: 支持多种导入方式
   - 节点链接
   - 订阅链接
   - 二维码扫描
   - 批量导入

### 9.3 代理配置方式

#### 9.3.1 透明代理（推荐）
- 优势：为所有程序提供代理服务
- 配置：在v2rayA设置中选择透明代理模式

#### 9.3.2 系统代理
- 适用：支持代理的程序
- 端口：20170(SOCKS5), 20171(HTTP)

#### 9.3.3 浏览器插件
- 推荐：SwitchyOmega
- 配置：使用v2rayA提供的本地端口

⚠️ **法律提醒**: 
- 请遵守当地法律法规
- 仅用于学习和技术研究
- 不得用于违法活动

---

## 10. 容器化环境

### 10.1 安装Docker

#### 10.1.1 设置Docker APT仓库

```bash
# 更新软件包索引并安装必要的包
sudo apt-get update
sudo apt-get install ca-certificates curl

# 添加Docker的官方GPG密钥
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# 添加仓库到APT源
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 更新软件包索引
sudo apt-get update
```

#### 10.1.2 安装Docker Engine

```bash
# 安装Docker及相关组件
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

#### 10.1.3 配置Docker

```bash
# 启动Docker服务
sudo systemctl start docker
sudo systemctl enable docker

# 将当前用户添加到docker组（避免每次使用sudo）
sudo usermod -aG docker $USER

# 注销并重新登录以使组更改生效
newgrp docker
```

#### 10.1.4 验证安装

```bash
# 验证Docker安装
docker --version
docker compose version

# 运行hello-world测试
docker run hello-world
```

### 10.2 Docker配置优化

#### 10.2.1 配置国内镜像加速

创建或编辑Docker daemon配置：
```bash
sudo mkdir -p /etc/docker
sudo vim /etc/docker/daemon.json
```

添加镜像源配置：
```json
{
  "registry-mirrors": [
    "https://docker.mirrors.ustc.edu.cn",
    "https://hub-mirror.c.163.com",
    "https://mirror.baidubce.com"
  ],
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m",
    "max-file": "3"
  }
}
```

重启Docker服务：
```bash
sudo systemctl daemon-reload
sudo systemctl restart docker
```

#### 10.2.2 Docker常用命令

```bash
# 查看容器
docker ps                 # 运行中的容器
docker ps -a             # 所有容器

# 查看镜像
docker images

# 容器操作
docker start <container>   # 启动容器
docker stop <container>    # 停止容器
docker restart <container> # 重启容器
docker rm <container>      # 删除容器

# 镜像操作
docker pull <image>        # 拉取镜像
docker rmi <image>         # 删除镜像

# 查看日志
docker logs <container>

# 进入容器
docker exec -it <container> /bin/bash
```

---

## 11. Node.js开发环境

### 11.1 使用NVM安装Node.js

#### 11.1.1 安装NVM

```bash
# 下载并安装NVM
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

# 重新加载配置
source ~/.bashrc

# 验证NVM安装
command -v nvm
```

#### 11.1.2 安装Node.js

```bash
# 安装指定版本的Node.js
nvm install 22.14.0

# 使用指定版本
nvm use 22.14.0

# 设置默认版本
nvm alias default 22.14.0

# 查看已安装的版本
nvm list

# 查看可用版本
nvm list-remote
```

#### 11.1.3 验证安装

```bash
# 检查Node.js版本
node -v      # 应该显示 v22.14.0

# 检查npm版本
npm -v       # 应该显示 10.9.2
```

#### 11.1.4 npm配置优化

```bash
# 配置npm国内镜像源
npm config set registry https://registry.npmmirror.com

# 查看配置
npm config get registry

# 安装cnpm（可选）
npm install -g cnpm --registry=https://registry.npmmirror.com
```

### 11.2 常用Node.js开发工具

```bash
# 全局安装常用工具
npm install -g yarn          # Yarn包管理器
npm install -g pm2           # 进程管理器
npm install -g nodemon       # 开发时自动重启
npm install -g typescript    # TypeScript编译器
npm install -g @vue/cli      # Vue CLI
npm install -g create-react-app  # React脚手架
```

---

## 12. 系统监控与维护

### 12.1 系统资源监控

#### 12.1.1 基础监控命令

```bash
# CPU和内存使用情况
top
htop    # 需要安装: sudo apt install htop

# 磁盘使用情况
df -h
du -sh /*

# 内存使用详情
free -h

# 网络连接
netstat -tuln
ss -tuln

# 进程监控
ps aux
pstree
```

#### 12.1.2 安装系统监控工具

```bash
# 安装常用监控工具
sudo apt install htop iotop nethogs glances

# htop - 进程监控
htop

# iotop - IO监控
sudo iotop

# nethogs - 网络使用监控
sudo nethogs

# glances - 综合监控
glances
```

### 12.2 日志管理

#### 12.2.1 系统日志查看

```bash
# 查看系统日志
sudo journalctl

# 查看特定服务日志
sudo journalctl -u ssh
sudo journalctl -u docker

# 实时查看日志
sudo journalctl -f

# 查看内核日志
dmesg

# 查看认证日志
sudo tail -f /var/log/auth.log
```

#### 12.2.2 日志轮转配置

```bash
# 查看logrotate配置
ls /etc/logrotate.d/

# 编辑logrotate主配置
sudo vim /etc/logrotate.conf
```

### 12.3 系统更新与维护

#### 12.3.1 系统更新

```bash
# 更新软件包列表
sudo apt update

# 升级所有软件包
sudo apt upgrade

# 升级系统版本（谨慎使用）
sudo apt dist-upgrade

# 清理不需要的软件包
sudo apt autoremove
sudo apt autoclean
```

#### 12.3.2 定期维护任务

创建维护脚本：
```bash
sudo vim /usr/local/bin/system-maintenance.sh
```

脚本内容：
```bash
#!/bin/bash
# 系统维护脚本

echo "开始系统维护..."

# 更新软件包列表
apt update

# 清理软件包缓存
apt autoremove -y
apt autoclean

# 清理临时文件
find /tmp -type f -atime +7 -delete

# 清理日志文件
journalctl --vacuum-time=30d

echo "系统维护完成"
```

设置权限并添加到定时任务：
```bash
sudo chmod +x /usr/local/bin/system-maintenance.sh

# 编辑crontab
sudo crontab -e

# 添加每周执行一次的维护任务
0 2 * * 0 /usr/local/bin/system-maintenance.sh >> /var/log/maintenance.log 2>&1
```

### 12.4 备份策略

#### 12.4.1 重要配置文件备份

```bash
# 创建备份目录
sudo mkdir -p /backup/configs

# 备份重要配置文件
sudo cp -r /etc/netplan/ /backup/configs/
sudo cp /etc/ssh/sshd_config /backup/configs/
sudo cp /etc/fstab /backup/configs/
sudo cp /etc/hosts /backup/configs/
```

#### 12.4.2 自动化备份脚本

```bash
sudo vim /usr/local/bin/config-backup.sh
```

脚本内容：
```bash
#!/bin/bash
BACKUP_DIR="/backup/configs/$(date +%Y%m%d)"
mkdir -p $BACKUP_DIR

# 备份配置文件
cp -r /etc/netplan/ $BACKUP_DIR/
cp /etc/ssh/sshd_config $BACKUP_DIR/
cp /etc/fstab $BACKUP_DIR/
cp /etc/hosts $BACKUP_DIR/

# 保留最近30天的备份
find /backup/configs/ -type d -mtime +30 -exec rm -rf {} \;
```

---

## 🔧 故障排除

### 网络问题排查

1. **检查网络接口状态**:
   ```bash
   ip link show
   ```

2. **检查IP配置**:
   ```bash
   ip addr show
   ```

3. **检查路由**:
   ```bash
   ip route show
   ```

4. **测试连通性**:
   ```bash
   ping 8.8.8.8
   ping google.com
   ```

5. **检查DNS解析**:
   ```bash
   nslookup google.com
   dig google.com
   ```

### SSH连接问题

1. **检查SSH服务状态**:
   ```bash
   sudo systemctl status ssh
   ```

2. **查看SSH日志**:
   ```bash
   sudo journalctl -u ssh
   ```

3. **检查防火墙**:
   ```bash
   sudo ufw status
   ```

### 磁盘空间问题

1. **查找大文件**:
   ```bash
   sudo find / -type f -size +100M 2>/dev/null
   ```

2. **清理系统缓存**:
   ```bash
   sudo apt clean
   sudo apt autoremove
   ```

3. **清理日志**:
   ```bash
   sudo journalctl --vacuum-size=100M
   ```

---

## 📚 学习资源

### 官方文档
- [Ubuntu官方文档](https://ubuntu.com/server/docs)
- [Systemd文档](https://systemd.io/)
- [Netplan文档](https://netplan.io/)

### 在线资源
- [Linux命令大全](https://www.runoob.com/linux/linux-command-manual.html)
- [Ubuntu中文论坛](https://forum.ubuntu.org.cn/)

---

## ⚠️ 安全提醒

1. **定期更新系统**：保持系统和软件包的最新状态
2. **强密码策略**：使用复杂密码，定期更换
3. **防火墙配置**：只开放必要的端口
4. **定期备份**：重要数据和配置文件要定期备份
5. **日志监控**：定期检查系统日志，及时发现异常
6. **权限管理**：遵循最小权限原则
7. **SSH安全**：使用密钥认证，禁用密码登录
   
---

<div align="center">

**📞 技术支持**

如需技术支持，请联系：fly910905@sina.com

**🎯 项目地址**: [AIAgent101](https://github.com/FlyAIBox/AIAgent101)

---

*本手册持续更新中，感谢你的关注与支持！* 🙏

</div> 

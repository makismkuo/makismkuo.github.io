---
title: "配一台个人服务器需要几步？Nginx + SSL + Docker 从零到上线"
date: 2026-05-23
draft: false
tags: ["部署", "服务器", "Nginx", "Docker", "运维"]
---

## 缘起

我一直想搞一台自己的服务器。需求很明确：能跑 Web 服务、国内访问速度快、不用操心备案的事。

国内服务器得走备案流程，阿里云和腾讯云我都试过，提交资料、等审核、管局核验，一套下来少说一两周。备案期间域名还不能解析，买了机器也只能干瞪眼。海外服务器倒是免备案，但美国、欧洲的节点延迟普遍在 150ms 以上，体验一般。

香港服务器是折中的最优解——免备案、延迟低（华南地区 < 20ms，北方也就 40-50ms）、带宽充足。虽然价格比同等配置的国内机器贵个 30% 左右，但省下来的时间成本完全值回票价。

最后我选了台 2 核 2G 的 HK 轻量云服务器，系统装的 Ubuntu 22.04 LTS。下面分享一下我的完整搭建过程。

## 一、SSH 安全加固：改端口 + 密钥登录

服务器拿到手的第一件事，不是装 Nginx，而是把 SSH 的大门关好。默认的 22 端口 + 密码登录太招摇了，我装好系统才半天，/var/log/auth.log 里就出现了几百条来自各种 IP 的暴力破解记录。

### 第一步：生成 SSH 密钥对（在本地执行）

```bash
ssh-keygen -t ed25519 -C "server-2026"
# 一路回车，会在 ~/.ssh/ 下生成 id_ed25519 和 id_ed25519.pub
# 然后把公钥传到服务器上
ssh-copy-id -i ~/.ssh/id_ed25519.pub root@你的服务器IP
```

Ed25519 比传统的 RSA 2048/4096 更安全，性能也更好，现在基本是标配了。

### 第二步：修改 SSH 配置

登录到服务器，编辑 `/etc/ssh/sshd_config`：

```bash
vim /etc/ssh/sshd_config
```

改动以下几项：

```
# 改端口，建议 1024-65535 之间选一个
Port 62222

# 禁止 root 直接登录（可选，视情况而定）
PermitRootLogin prohibit-password

# 禁止密码登录
PasswordAuthentication no

# 使用密钥登录
PubkeyAuthentication yes

# 只允许特定用户登录（可选）
AllowUsers 你的用户名
```

改完重启 SSH 服务：

```bash
systemctl restart sshd
```

**注意**：在退出当前 SSH 会话之前，一定要**新开一个终端窗口**测试一下能否用密钥登录成功。万一配置写错了，你还有退路。别问我怎么知道的……

### 第三步：配置防火墙

Ubuntu 自带 ufw，配置起来很简单：

```bash
# 先开放修改后的 SSH 端口，再启用防火墙——顺序很重要
ufw allow 62222/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable

# 查看防火墙状态
ufw status verbose
```

如果以后还要跑其他服务，记得把对应端口加进去。我目前只开放了 22（改后的端口）、80、443，够用了。

做完这三步，服务器的安全基线就搭好了。日志里的扫描记录肉眼可见地减少了。

## 二、Nginx：统一的流量入口

Nginx 是我最喜欢的反向代理工具，配置简洁、性能强悍。我的设计思路是：**所有外部请求统一先到 Nginx，Nginx 根据域名把请求分发到不同的后端服务**。

### 安装 Nginx

```bash
apt update
apt install nginx -y
systemctl enable nginx
systemctl start nginx
```

### 配置站点

Nginx 的站点配置文件放在 `/etc/nginx/sites-available/`，启用后软链接到 `/etc/nginx/sites-enabled/`。

我的服务器上绑了三个域名，对应三个不同的服务。先创建一个主配置文件：

```bash
vim /etc/nginx/sites-available/aibestapp
```

主站是一个静态网站，直接指向本地文件目录：

```nginx
server {
    listen 80;
    server_name aibestapp.top www.aibestapp.top;

    root /var/www/aibestapp;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

博客是通过 Nginx 反代到 GitHub Pages：

```nginx
server {
    listen 80;
    server_name blog.aibestapp.top;

    location / {
        proxy_pass https://你的用户名.github.io;
        proxy_set_header Host 你的用户名.github.io;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

统计分析用的是 Umami，跑在 Docker 里，监听本机 3000 端口：

```nginx
server {
    listen 80;
    server_name stats.aibestapp.top;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

配置写好后，启用站点并检查语法：

```bash
ln -s /etc/nginx/sites-available/aibestapp /etc/nginx/sites-enabled/
nginx -t          # 检查语法，没有报错再继续
systemctl reload nginx
```

## 三、SSL 证书：certbot 一键搞定

以前配 HTTPS 是个挺折腾的事——先花钱买证书，然后把证书文件上传到服务器，配置 Nginx 的 ssl_certificate 和 ssl_certificate_key，还要记着三个月或一年后手动续期。现在有了 certbot，这些全自动化了。

### 安装 certbot

```bash
apt install certbot python3-certbot-nginx -y
```

### 申请证书

一条命令搞定：

```bash
certbot --nginx -d aibestapp.top -d www.aibestapp.top
```

certbot 会自动检测 Nginx 配置，修改 server block 加入 SSL 相关配置，还会帮你做 HTTP 到 HTTPS 的 301 跳转。整个过程不到 30 秒，命令行里会输出绿色的 "Congratulations!"。

其他域名同理：

```bash
certbot --nginx -d blog.aibestapp.top
certbot --nginx -d stats.aibestapp.top
```

### 自动续期

Let's Encrypt 的证书有效期是 90 天，但 certbot 自带续期逻辑。系统里会自动安装一个 systemd timer：

```bash
# 查看 timer 状态
systemctl status certbot.timer

# 手动测试续期（不会真的续期，只是模拟）
certbot renew --dry-run
```

续期后 certbot 会自动 reload Nginx 让新证书生效，什么都不用管。我用了一年多，从来没操心过证书过期的问题。

### 验证 SSL

证书配好后，可以用 ssllabs.com 的在线工具测一下安全评级，或者在本地 curl 验证：

```bash
curl -I https://aibestapp.top
# 返回 200 OK 和 SSL 相关信息
```

## 四、Docker：隔离环境，方便迁移

对于需要数据库后端的服务，用 Docker 管理是最省心的。一个 docker-compose.yml 文件定义好所有依赖，一键启动。哪天不想用了，一条命令全部清掉，系统干干净净。

### 安装 Docker

```bash
# 安装依赖
apt install apt-transport-https ca-certificates curl software-properties-common -y

# 添加 Docker 官方 GPG 密钥
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -

# 添加 Docker 仓库
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# 安装 Docker
apt update
apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin -y

# 验证安装
docker --version
docker compose version
```

### 用 Docker Compose 部署 Umami

Umami 是一个开源的网站统计分析工具，用 Node.js 写的，界面清爽，功能够用。它需要两个服务：Umami 本身和 PostgreSQL 数据库。

在 `/opt/umami/` 目录下创建 `docker-compose.yml`：

```yaml
version: '3.8'

services:
  umami-db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: umami
      POSTGRES_USER: umami
      POSTGRES_PASSWORD: 你的密码
    volumes:
      - umami-db-data:/var/lib/postgresql/data
    restart: always
    networks:
      - umami-net

  umami:
    image: ghcr.io/umami-software/umami:postgresql-latest
    ports:
      - "127.0.0.1:3000:3000"
    environment:
      DATABASE_URL: postgresql://umami:你的密码@umami-db:5432/umami
      DATABASE_TYPE: postgresql
      APP_SECRET: 随机生成的一串密钥
    depends_on:
      - umami-db
    restart: always
    networks:
      - umami-net

volumes:
  umami-db-data:

networks:
  umami-net:
```

注意 `ports` 那行我写的是 `127.0.0.1:3000:3000`，意思是 Umami 只监听本机，不对外暴露端口。外部请求统一走 Nginx 反代，安全性更好。

启动：

```bash
cd /opt/umami
docker compose up -d
docker compose ps    # 确认两个容器都在运行
```

### Docker 运维小技巧

几个常用的命令：

```bash
# 查看容器日志（实时）
docker compose logs -f

# 更新镜像
docker compose pull
docker compose up -d

# 停掉并删除所有容器和数据
docker compose down -v

# 清理无用镜像和缓存
docker system prune -a
```

## 五、非 Docker 服务：systemd 管理

不是所有服务都适合跑在 Docker 里。像我的 Telegram Bot 和交易机器人，本身就是编译好的二进制文件，直接跑 systemd 更轻量。

以 Telegram Bot 为例，创建一个 systemd 服务文件 `/etc/systemd/system/telegram-bot.service`：

```ini
[Unit]
Description=Telegram Bot Service
After=network.target

[Service]
Type=simple
User=bot
WorkingDirectory=/opt/telegram-bot
ExecStart=/opt/telegram-bot/bot
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

启动并设置开机自启：

```bash
systemctl daemon-reload
systemctl enable telegram-bot
systemctl start telegram-bot
systemctl status telegram-bot
```

查看日志用 journalctl：

```bash
journalctl -u telegram-bot -f
```

这种方式的优点是资源占用极低，管理也方便。交易机器人也是同样的套路。

## 六、目前跑了哪些服务

| 服务 | 域名 | 部署方式 | 资源占用 |
|------|------|---------|---------|
| 主站 | aibestapp.top | Nginx 静态文件 | 极低，纯文件 IO |
| 博客 | blog.aibestapp.top | Nginx → GitHub Pages | 几乎为零，流量穿透 |
| 统计分析 | stats.aibestapp.top | Nginx → Docker (Umami + PostgreSQL) | 中，数据库占内存大头 |
| Telegram Bot | — | systemd | 低，纯 API 调用 |
| 交易机器人 | — | systemd | 低，定时任务为主 |

## 七、实际运行表现

这台 2 核 2G 的 HK 服务器已经稳定跑了半年多。日常负载情况：

- **CPU**：常年在 10%-15% 之间徘徊，偶尔有瞬时尖峰到 30%
- **内存**：used 约 800MB-1GB，还剩 1GB 左右空闲
- **磁盘**：用了不到 20GB（主要是 Docker 镜像和日志）

还有不少余量。如果以后有新的服务需求，大概率能继续往上堆。

## 八、一些运维心得

1. **端口改掉真的有用**。改 SSH 端口之后，auth.log 里的暴力破解记录从每天几百条降到了个位数。

2. **Nginx 做统一入口的好处**。你不需要记住每个服务跑在哪个端口，所有外部流量统一走 80/443，内部服务可以随意换端口，对用户完全透明。

3. **Docker 不要对外暴露端口**。Docker 容器只监听 127.0.0.1，前端统一走 Nginx 反代。这样防火墙规则很简单，也少了很多攻击面。

4. **系统更新别偷懒**。每个月跑一次 `apt update && apt upgrade`，Docker 镜像也定期 `docker compose pull` 更新。安全补丁这种东西，早打早安心。

5. **一台机器够用就不要上集群**。个人项目真没必要搞 K8s 那一套。我见过有人就跑了两个静态页面，硬上三台机器搭 K8s 集群，运维成本比开发成本还高。**够用就好，别过度配置。**

目前这五个服务在一台 2 核 2G 的机器上跑得很舒服，日常维护也就是看看日志、更新一下系统。要是哪天服务量翻倍了，再考虑横向扩展也不迟。

---
title: "一个 HK 服务器的自我修养：Nginx 到 Docker"
date: 2026-05-23
draft: false
tags: ["部署", "服务器", "Nginx", "Docker"]
---

## 开头

买了一台 HK 服务器，2 核 2G，心想：能不能把能跑的服务全塞进去？

答案是：能。而且还有余量。

## 第一步：基础安全

装好系统第一件事，关密码登录、开 SSH 密钥。密码登录就像家里大门的锁是纸糊的——明明知道不安全，但很多人就是不改。

```bash
# 改 SSH 端口
# 禁止密码登录
# 防火墙只开 22/80/443
```

## Nginx：所有网站的入口

一台服务器跑多个网站，Nginx 就是那个"门卫大爷"。每个访客来了，它看一眼域名，指向对应的服务：

- `aibestapp.top` → 静态文件目录
- `blog.aibestapp.top` → 反代到 GitHub Pages
- `stats.aibestapp.top` → 反代到 Umami Docker 容器

## SSL：LetsEncrypt 永远的神

```bash
certbot --nginx -d example.com
```

一行命令，证书到手，自动续期。以前买 SSL 证书一年几百块，现在免费的质量更好。

## Docker：隔离的艺术

所有后端服务都走 Docker Compose。好处是：想删就删，想重装就重装，宿主机干干净净。

## 都跑了什么

| 服务 | 方式 |
|------|------|
| 主站 aibestapp.top | Nginx 静态文件 |
| 博客反代 | Nginx → GitHub Pages |
| 统计分析 | Docker → Umami |
| Telegram Bot | systemd 进程 |
| 交易机器人 | systemd 进程 |

2 核 2G 跑 5 个服务，CPU 常年 20% 以下。有时候觉得自己买的不是服务器，是寂寞。

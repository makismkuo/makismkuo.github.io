---
title: "配一台个人服务器需要几步？Nginx + SSL + Docker"
date: 2026-05-23
draft: false
tags: ["部署", "服务器", "Nginx", "Docker", "运维"]
---

## 缘起

需要一个能跑服务、国内访问快、免备案的服务器。HK 服务器是最优解。

## 基础配置清单

### 1. 初始安全

```bash
# 改 SSH 端口 + 密钥登录（禁止密码）
# 开防火墙：仅开放 22/80/443
```

### 2. Nginx

作为所有网站的统一入口，反向代理到各个后端服务。

### 3. SSL 证书

```bash
certbot --nginx -d example.com
```

一次申请，自动续期。所有子域名都走 HTTPS。

### 4. Docker

后端服务全部走 Docker Compose，隔离环境、方便迁移。

## 跑了哪些服务

| 服务 | 域名 | 方式 |
|------|------|------|
| 主站 | aibestapp.top | Nginx 静态文件 |
| 博客反代 | blog.aibestapp.top | Nginx → GitHub Pages |
| 统计分析 | stats.aibestapp.top | Nginx → Umami (Docker) |
| Telegram Bot | — | systemd 进程 |
| 交易机器人 | — | systemd 进程 |

## 心得

一台 2 核 2G 的 HK 服务器，跑了 5 个服务还有余量。对于个人项目来说，**够用就好，别过度配置**。

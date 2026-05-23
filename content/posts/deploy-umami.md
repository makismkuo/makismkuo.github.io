---
title: "自建 Umami 网站统计分析：Docker + Nginx + Certbot"
date: 2026-05-23
draft: false
tags: ["部署", "Umami", "Docker", "Nginx"]
---

## 为什么自建

Google Analytics 太臃肿，Plausible 要付费。Umami 是开源的轻量级替代，自建零成本。

## 部署步骤

### 1. Docker Compose 一键启动

```yaml
version: '3'
services:
  umami:
    image: ghcr.io/umami-software/umami:postgresql-latest
    ports:
      - "127.0.0.1:3000:3000"
    environment:
      DATABASE_URL: postgresql://umami:umami@db:5432/umami
      DATABASE_TYPE: postgresql
      APP_SECRET: your-secret
    depends_on:
      - db
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: umami
      POSTGRES_USER: umami
      POSTGRES_PASSWORD: umami
    volumes:
      - umami-db-data:/var/lib/postgresql/data
```

### 2. Nginx 反代（绑域名 + SSL）

用 Certbot 自动申请证书，niginx 反代到 `127.0.0.1:3000`，域名挂 `stats.aibestapp.top`。

### 3. 避坑

- Umami v3 登录**用的是用户名**（不是邮箱）
- 默认账号 `admin` / `umami`，首次登录记得改密码
- Docker 映射务必 `127.0.0.1:3000`，不要暴露公网端口

## 效果

目前稳定运行，每天看得到各个页面的访问数据。轻量、够用、免费。

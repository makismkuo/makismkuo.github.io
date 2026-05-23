---
title: "自建 Umami：跟 Google Analytics 说再见"
date: 2026-05-23
draft: false
tags: ["部署", "Umami", "Docker", "Nginx"]
---

## 为什么选择 Umami

网站的访问统计是个很有意思的需求——你明知道看了也改变不了什么，但每天还是想打开看一眼。

之前用 Google Analytics，功能确实强大，但总觉得它像一个穿着西装的推销员，每次来都带着一堆你不需要的东西。页面加载慢、配置项多、数据面板复杂，我只是想知道昨天有多少人访问而已。

后来试了 Plausible，体验很好，简洁干净。但它是付费服务，按年收费。不是说付不起，而是想到这笔钱可以买别的，就犹豫了。

Umami 是 Plausible 的开源替代品。功能上差不多——访问量、页面排名、来源渠道、访客设备，该有的都有。最重要的区别是：它免费。

## 部署过程

Umami 官方推荐用 Docker Compose 部署。如果服务器上已经装了 Docker，这一步基本不费什么功夫。

```yaml
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

这里有个小细节值得注意：端口映射写的是 `127.0.0.1:3000:3000`，意思是只在本地监听 3000 端口，不暴露到公网。加上 Nginx 反代后，外部访问只能通过域名和 HTTPS 进来，安全性多了一层。

## Nginx 反代与 SSL

在 Nginx 配置里加上：

```nginx
server {
    server_name stats.aibestapp.top;
    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

然后用 certbot 申请证书：

```bash
certbot --nginx -d stats.aibestapp.top
```

整个过程大概五分钟。Certbot 会自动修改 Nginx 配置、添加 SSL 相关指令，还会设置定时任务自动续期。

## 使用感受

Umami 的界面非常简洁。左侧是菜单栏，右侧是数据展示。没有花哨的图表动画，没有弹窗引导教程，就是干净的数据。

登录的时候有个小插曲。Umami v3 版本的用户名不是邮箱，而是直接设的用户名。我拿着邮箱输了半天没进去，一度怀疑自己是不是搭错了。后来去文档翻了一下才发现——默认账号是 `admin`，密码是 `umami`。

进去之后第一件事就是改密码。

## 目前的状态

运行了一段时间，没有出过问题。每次打开能看到昨天有多少人访问、从哪来的、看了哪些页面。数据不多，但对于个人网站来说足够了。

如果要给 Umami 打分，10 分我会给 8 分。扣掉的 2 分给界面——虽然干净，但有点太干净了，有时候找设置项要找一会儿。

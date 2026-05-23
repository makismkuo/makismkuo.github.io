---
title: "自建 Umami：跟 Google Analytics 说再见"
date: 2026-05-23
draft: false
tags: ["部署", "Umami", "Docker", "Nginx"]
---

## 为什么要自建统计

以前用 Google Analytics，每次打开都想骂人——页面加载慢得像在拨号上网，数据面板复杂得能当考卷。我就想知道多少人看了我的网站，至于给我整一套航天飞机操作台吗？

后来试了 Plausible，好用，但要钱。一年几十刀倒也不贵，但一想到"这笔钱本来可以吃顿好的"，我就犹豫了。

直到遇到 Umami。

它像一个刚毕业的大学生——干净、清爽、不整活。打开页面，数据就在那，不多不少。

## 部署过程

### Docker Compose

说实话，第一次部署我栽了个跟头。Umami 需要 PostgreSQL，但我 docker-compose.yml 里把数据库密码写成了弱密码 `umami`，心里总觉得不安——虽然这个数据库只监听本地端口。

配置很简单：

```yaml
services:
  umami:
    image: ghcr.io/umami-software/umami:postgresql-latest
    ports:
      - "127.0.0.1:3000:3000"
    environment:
      DATABASE_URL: postgresql://umami:umami@db:5432/umami
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: umami
      POSTGRES_PASSWORD: umami
```

### Nginx 反代

Umami 装在 3000 端口，但我不想直接暴露端口——万一来个扫描器给我整出事儿呢？所以用 Nginx 做反向代理，绑定域名 `stats.aibestapp.top`，套上 SSL。

```bash
certbot --nginx -d stats.aibestapp.top
```

一行命令，证书到手。Certbot 是我见过最良心的工具——不要钱、不要注册、一次性搞定。

## 踩坑记录

**最大一个坑：Umami v3 登录用的是用户名，不是邮箱。**

我盯着登录界面看了五分钟，试了三遍邮箱都不对，心想"完了，数据库炸了"。最后翻文档才发现——用户名是 `admin`，密码是 `umami`。

登录进去那一刻，感觉自己像个傻子。

## 目前的状态

稳定运行中，每天看看访问量，够用。如果你也想要一个不折腾的统计分析工具，Umami 值得一试。

对了，记得改默认密码——不然你跟我一样傻。

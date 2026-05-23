---
title: "在 HK 服务器上搭了一套基础架构"
date: 2026-05-23
draft: false
tags: ["部署", "服务器", "Nginx", "Docker"]
---

## 选服务器的思路

做个人项目的时候，服务器的选择会直接影响后期的运维成本。

国内服务器需要备案，流程走下来少说一两周。而且备案期间域名不能访问，等于买了一台空机器放在那干等。海外服务器免备案，即买即用，但延迟相对高一些。

香港服务器算是中间方案——免备案、延迟低、国内访问速度快。虽然价格比国内同等配置贵一些，但省下来的时间成本是值得的。

## 基础配置流程

### 安全设置

系统装好后，第一步是加固 SSH 安全。默认的 22 端口和密码登录方式不太安全，每天都能在日志里看到各种扫描和暴力破解的尝试。

```bash
# 修改 SSH 端口
# 关闭密码登录，改用密钥
# 配置防火墙，仅开放 22、80、443
```

这几步做完之后，日志里的扫描记录明显少了。

### Nginx

Nginx 作为统一的流量入口，负责接收所有 HTTP 请求，然后根据域名分发到不同的后端服务。

这台服务器上目前绑了三个域名，每个域名对应不同的服务。Nginx 通过 `server_name` 来区分请求应该转发到哪。

```nginx
server {
    server_name aibestapp.top;
    root /var/www/aibestapp;
}

server {
    server_name blog.aibestapp.top;
    location / {
        proxy_pass https://github.io;
    }
}

server {
    server_name stats.aibestapp.top;
    location / {
        proxy_pass http://127.0.0.1:3000;
    }
}
```

### SSL 证书

以前 SSL 证书是个麻烦事——要购买、要手动部署、要记得续期。现在这些事 certbot 全包了。

```bash
certbot --nginx -d example.com
```

运行一次，HTTPS 就配好了。证书三个月到期，certbot 会自动续期。

### Docker

对于需要数据库后端的服务（比如 Umami），用 Docker 来管理是最省心的。一个 docker-compose.yml 文件定义了所有依赖，哪天不想用了，一条命令全部清掉，不会在系统里留下什么痕迹。

## 这台服务器上跑了什么

| 服务 | 方式 | 占用 |
|------|------|------|
| 主站 aibestapp.top | Nginx 静态文件 | 低 |
| 博客反代 blog.aibestapp.top | Nginx 反代 | 极低 |
| 统计分析 stats.aibestapp.top | Docker (Umami) | 中 |
| Telegram Bot | systemd | 低 |
| 交易机器人 | systemd | 低 |

2 核 2G 的配置跑这些服务，CPU 常年稳定在 15% 以下，内存使用不到 1GB。对于个人项目来说，这个配置是够用的。

## 运维方面的思考

一台服务器跑太多服务确实存在风险——某个服务出问题可能会影响其他服务。我的做法是把服务按重要性分开管理：核心服务（网站、博客）走 Nginx 静态部署，稳定性最高；开发工具（分析、Bot）走 Docker 或 systemd，方便更新和调试。

如果未来服务继续增加，可能会考虑拆到多台机器上。不过目前这个阶段，一台机器足够了。

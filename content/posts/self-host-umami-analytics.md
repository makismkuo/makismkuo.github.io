---
title: "自建 Umami 网站统计分析：Docker + Nginx + Certbot"
date: 2026-05-23
draft: false
tags: ["部署", "Umami", "Docker", "Nginx"]
---

## 为什么自建

网站访问统计这件事，说大不大，说小不小。我之前的方案是 Google Analytics，功能确实强，但体感上越来越重——每次加载都要拖慢页面，控制台里几十个报表模板，我只是想知道昨天有多少访客、看了哪些页面而已。

后来试了 Plausible，干净利落，体验很好。但它是付费服务，按年收费。不是说付不起，而是想到这笔钱可以买一台小服务器跑点别的，就觉得自建更划算。

Umami 正是这个定位下的最佳选择。开源、轻量、免费，功能上覆盖了个人网站需要的所有统计维度：访问量、页面排名、来源渠道、访客设备、操作系统、浏览器版本等等。而且它支持多站点管理，一个实例可以同时跟踪多个网站的数据。

## 环境准备

部署之前，确认服务器上已经安装好以下组件：

- **Docker** 和 **Docker Compose**（用于启动 Umami 和 PostgreSQL）
- **Nginx**（用于反向代理）
- **域名**（已解析到服务器 IP）

我用的是 Ubuntu 22.04 系统，如果你用的是其他 Linux 发行版，安装命令略有不同，但后面的 Docker Compose 和 Nginx 配置是通用的。

## Docker Compose 部署

Umami 官方推荐用 Docker Compose 部署，这也是最省心的方式。创建一个目录来存放配置：

```bash
mkdir ~/umami && cd ~/umami
```

然后新建 `docker-compose.yml` 文件，写入以下内容：

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
    restart: always

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: umami
      POSTGRES_USER: umami
      POSTGRES_PASSWORD: umami
    volumes:
      - umami-db-data:/var/lib/postgresql/data
    restart: always

volumes:
  umami-db-data:
```

有几个配置项需要留意一下。

**`APP_SECRET`** 用于加密会话和 JWT Token，建议用一个足够随机的字符串，可以用 `openssl rand -base64 32` 生成。

**端口映射 `127.0.0.1:3000:3000`**，意思是 Docker 容器内的 3000 端口只映射到本机的回环地址。这样外部网络无法直接访问 Umami 的管理界面，必须通过 Nginx 反向代理才能到达，安全性更高。如果直接写成 `3000:3000`，就等于把管理后台暴露在了公网上，不建议这么做。

**`restart: always`** 确保服务器重启后容器自动启动，不用手动干预。

保存文件后，执行：

```bash
docker compose up -d
```

第一次运行会拉取镜像，等一两分钟后，在服务器本地验证：

```bash
curl http://127.0.0.1:3000
```

如果返回 HTML 内容，说明 Umami 已经正常运行了。

## Nginx 反向代理与 SSL

Umami 启动之后，需要通过域名加 HTTPS 来访问。用 Nginx 做反向代理，把请求转发到本地的 3000 端口。

新建 Nginx 配置文件：

```bash
sudo nano /etc/nginx/sites-available/umami
```

写入以下内容：

```nginx
server {
    listen 80;
    server_name stats.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

`proxy_set_header` 这几行很关键。如果不传 `X-Forwarded-For` 和 `X-Forwarded-Proto`，Umami 获取到的访客 IP 全是 Nginx 本机地址，没法正确统计来源地域。同时，缺少 `X-Forwarded-Proto` 会导致 Umami 认为请求是 HTTP 而非 HTTPS，可能引发回调 URL 协议不匹配的问题。

启用配置并测试：

```bash
sudo ln -s /etc/nginx/sites-available/umami /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

接着用 Certbot 自动申请 SSL 证书：

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d stats.yourdomain.com
```

Certbot 会交互式询问邮箱（用于接收证书到期通知），然后自动验证域名所有权、申请证书、修改 Nginx 配置加入 SSL 相关指令。完成后用浏览器访问 `https://stats.yourdomain.com` 就能看到 Umami 的登录页面了。

Certbot 还会自动添加一个定时任务到 `/etc/cron.d/certbot`，每天检查证书有效期，到期前自动续签。基本上配置好之后就不用再管了。

## 避坑：Umami v3 登录细节

部署成功后遇到的第一个坑是登录。Umami v3 版本的登录用户名不是邮箱，而是直接设置的**用户名**。默认账号是 `admin`，密码是 `umami`。

我刚开始拿着邮箱试了好几次都提示登录失败，一度怀疑自己部署出错了。后来翻文档才发现用户名和邮箱在 Umami v3 里是两个不同的字段。登录框里填的是用户名，不是邮箱地址。

进去之后第一件事就是改密码。在左侧菜单找到 Settings → Profile，修改默认密码。这一步建议立刻做，因为默认密码 `umami` 是公开的，任何知道你域名的人都可以用 `admin` / `umami` 登录进去。

另外，Umami 默认开启注册功能，也就是说任何人都可以注册账号。如果不需要多人协作，可以在 Admin → Settings 里关闭 Allow New Registrations。这一步也建议在部署完成后立即操作。

## 接入网站

登录 Umami 后，点击 Add Site，输入网站名称和域名，系统会生成一段跟踪代码：

```html
<script defer src="https://stats.yourdomain.com/script.js" data-website-id="YOUR_SITE_ID"></script>
```

把这段脚本放到网站的 `<head>` 或 `<body>` 标签里即可。Umami 的脚本非常轻量，压缩后只有 2KB 左右，对页面加载速度几乎没有影响。

如果是 Hugo 这类静态网站，可以把跟踪代码放在 `layouts/partials/` 下的公共模板里，方便全局引入。比如新建 `layouts/partials/umami.html`，然后在 `baseof.html` 中用 `{{ partial "umami.html" . }}` 引用。

## 使用感受

Umami 的界面设计走的是极简路线。左侧菜单栏分类清晰：Dashboard（概览）、Realtime（实时）、Websites（站点管理）、Settings（设置）。右侧数据展示区域没有花哨的图表动画，就是干净的折线图和数字。

Dashboard 默认展示最近 30 天的数据，包含：

- **页面浏览量**（Pageviews）和**独立访客**（Unique Visitors）
- **来源渠道**（Referrers）：从搜索引擎来的、从其他网站跳转来的、直接访问的
- **页面排名**（Pages）：哪些页面被访问最多
- **设备分类**（Devices）：桌面端、移动端、平板的比例
- **操作系统**和**浏览器**分布

实时面板（Realtime）可以看到当前在线人数和正在访问的页面，延迟在几秒以内。

数据不多，但对于个人博客或小网站来说完全够用。每天打开看一眼昨天有多少人访问、从哪来的、看了哪些文章，心里有个大概就好。

运行了一段时间，没有出过问题。容器内存占用大约 120MB，PostgreSQL 再加 80MB，对于一台 1GB 内存的轻量云服务器来说很轻松。

给 Umami 打分的话，10 分我会给 8 分。功能、性能、稳定性都没问题。扣掉的 2 分给用户界面——虽然干净是好事，但有时候过于简洁了，比如找网站设置项要翻一会儿，筛选时间范围的操作也不够直观。不过这些都是小问题，不影响日常使用。

如果你也在找一个免费、轻量、能自己掌控数据的网站统计方案，Umami 值得一试。

---
title: "Hugo 博客搭建：从零到国内可访问的全过程"
date: 2026-05-23
draft: false
tags: ["部署", "Hugo", "GitHub", "博客"]
---

大家好，我是一凡。这篇博客记录了我用 Hugo + PaperMod 搭建技术博客的完整过程，包括选型思路、架构设计、配置细节和踩坑记录。希望对正在折腾博客的朋友有帮助。

## 为什么最终选了 Hugo

市面上静态博客生成器不少，我逐一试过，说说我个人的感受。

**Jekyll** 是老牌选手，GitHub Pages 原生支持，生态成熟。但它基于 Ruby，本地环境配置比较折腾，我每次换电脑都要重新装 Ruby 和 bundle，而且编译速度慢，几百篇文章要等十几秒，迭代体验不好。

**Hexo** 基于 Node.js，社区主题丰富，中文资料也多。但它的编译速度随着文章增多下降明显，而且依赖 node_modules，一旦依赖版本冲突就头疼。另外它的配置文件结构个人感觉偏重，不太直观。

**Astro** 比较新，设计理念很好，支持岛屿架构，可以做很复杂的页面。但对于一个纯博客来说有点杀鸡用牛刀了。Astro 的构建依赖 npm，项目体积也大，而且学习曲线相对陡，为了写个博客去学一套新框架，感觉有点划不来。

**Hugo** 吸引我的地方有几个：编译极快，我目前几十篇文章，构建时间在 100ms 左右，基本是瞬间完成；单二进制文件，没有运行环境依赖，macOS 上 brew install hugo 就搞定；模板语法虽然有点怪，但配置本身很简单，一个 config.yaml 就能跑起来。

至于主题，我选的是 **PaperMod**。它是 Paper 主题的维护升级版，GitHub 上 10k+ star，社区活跃，基本周更。功能上该有的都有：暗黑模式、全文搜索、代码复制按钮、目录 TOC、RSS 订阅，而且 UI 干净，不花哨，对阅读体验友好。

## 需求拆解与方案设计

动手之前，我先把博客的需求列了一下，避免后面跑偏：

1. **零成本托管** —— 博客没有营收，不想每个月掏服务器钱
2. **国内能正常访问** —— 我的读者大部分在国内，如果打不开等于白写
3. **写作流程越简单越好** —— 最好是本地写 Markdown，推送即更新
4. **域名统一品牌** —— 博客用子域名挂在我主站品牌下

这四条的最终方案分别是：

- 托管 → **GitHub Pages**，完全免费，香港和日本节点访问速度尚可
- 国内访问 → **香港轻量服务器 Nginx 反向代理**，几十块钱一个月，只转发静态文件，负载极低
- 自动化 → **GitHub Actions**，推 main 分支自动构建部署
- 域名 → **blog.aibestapp.top**，跟主站同一域名体系

这里说一个小细节。GitHub Pages 默认绑定的是 `username.github.io` 这种域名，你可以绑自定义域名，但 GitHub 的 IP 在国内部分地区会被墙或者丢包严重。即使绑了自定义域名，国内访问还是不稳定。所以我干脆让它走 GitHub Pages 的原生域名，然后在前面加一层香港反代，这样国内访问走反代，国外直接访问 GitHub Pages，两边都不受影响。

## 整体部署架构

来看一下整体流程：

```
本地写 .md → git push → GitHub
                          ↓
                 GitHub Actions 自动构建
                          ↓
          ┌─── GitHub Pages（海外用户直接访问）
          │
          └─── 香港 Nginx 反代 GitHub Pages（国内用户）
                          ↓
                   blog.aibestapp.top（统一入口）
```

这里有一个关键设计：**内容只存一份**。所有文章都在 GitHub 仓库里，GitHub Actions 构建后部署到 Pages。香港服务器上 Nginx 只是做了反向代理，指向 GitHub Pages 的原始地址，本身不存任何内容。这样做的好处是维护成本极低——我只需要维护一个代码仓库和一个 Nginx 配置文件。

代价是单点故障。如果 GitHub 宕机或者被墙加重，两个入口都会受影响。对我个人博客来说这个风险可以接受。

## 详细配置过程

### 1. 初始化 Hugo 项目

```bash
# 安装 Hugo（macOS）
brew install hugo

# 创建新站点
hugo new site blog --format yaml
cd blog

# 初始化 git 仓库
git init
```

这里我指定了 `--format yaml`，Hugo 默认用 TOML，但我更习惯 YAML 的缩进风格，可读性好一些。

### 2. 安装 PaperMod 主题

我用的方式是用 git submodule，这样主题和内容分离，后续更新主题只需 pull 一下：

```bash
git submodule add https://github.com/adityatelange/hugo-PaperMod themes/PaperMod
```

如果你直接用 `git clone` 把主题文件放进来，主题就变成了你仓库的一部分。后续主题作者更新了 bug 修复或新功能，你需要手动对比文件差异再合并，比较麻烦。submodule 的话一行命令就能同步：

```bash
git submodule update --remote
```

### 3. Hugo 配置文件

这是 `config.yaml` 的核心部分。PaperMod 的参数比较多，我挑关键的说：

```yaml
baseURL: "https://makismkuo.github.io/"
languageCode: zh-cn
title: "一凡的技术博客"
theme: PaperMod

params:
  homeInfoParams:
    Title: "你好，我是一凡"
    Content: "记录技术思考、项目经验和踩坑记录"
  socialIcons:
    - name: github
      url: "https://github.com/makismkuo"
    - name: rss
      url: "/index.xml"

  # 搜索
  search: true
  fuseOpts:
    isCaseSensitive: false
    threshold: 0.2

  # 暗黑模式
  disableThemeToggle: false

  # 文章目录
  showToc: true
  tocOpen: false

  # 代码复制按钮
  showCodeCopyButtons: true

outputs:
  home:
    - HTML
    - RSS
    - JSON
```

这里要特别注意 `baseURL`。因为我是用 GitHub Pages 托管，所以 baseURL 填的是 GitHub Pages 分配的地址 `https://makismkuo.github.io/`。如果填了自定义域名，PaperMod 生成的 RSS feed 链接和 sitemap 里的 URL 会全部变成自定义域名，而反代那边的 URL 解析可能出现不一致。保持 baseURL 指向实际托管地址是最稳妥的做法。

另外 `outputs` 里加了 JSON，这是 PaperMod 全文搜索功能所依赖的。Hugo 会生成一个 `index.json` 文件，包含所有文章内容和元数据，搜索时前端 JavaScript 读取这个文件做本地模糊匹配。PaperMod 用的是 Fuse.js 这个库，搜索体验接近即时，不需要后端服务。

### 4. 创建搜索页面

这一步容易漏掉。配了 `search: true` 之后，还需要在 content 目录下手动创建搜索页面，否则导航栏里不会出现搜索入口：

```bash
hugo new search.md
```

然后在 `content/search.md` 里写入：

```yaml
---
title: "搜索"
layout: "search"
---
```

这里 `layout: search` 告诉 PaperMod 使用主题自带的搜索模板来渲染这个页面。如果漏了这一页，配置里的 `search: true` 是不生效的。

### 5. GitHub Actions 自动化部署

配置文件 `.github/workflows/deploy.yml`：

```yaml
name: Deploy Hugo site to Pages

on:
  push:
    branches: ["main"]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: recursive
          fetch-depth: 0

      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v2
        with:
          hugo-version: "latest"
          extended: true

      - name: Build
        run: hugo --minify

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./public

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

说几个容易踩坑的点：

第一，`actions/checkout@v4` 必须加上 `submodules: recursive`，否则 submodule 引入的 PaperMod 主题不会被拉下来，构建时会报主题找不到的错误。

第二，`fetch-depth: 0` 是为了让 Hugo 在构建时生成正确的 .GitInfo 和最后修改时间。如果不加这个参数，浅克隆会导致所有页面显示同一时间。

第三，我用的是 `peaceiris/actions-hugo@v2` 这个第三方 action，它支持指定 Hugo 版本和扩展版。`extended: true` 很重要，PaperMod 用到了 Hugo 的 Sass/SCSS 处理能力，标准版不支持，必须用 extended 版本才能正常渲染主题样式。

第四，`hugo --minify` 会对 HTML、CSS、JS 做压缩。我实测大概能减少 15%-20% 的体积，对页面加载速度有帮助。不过 minify 偶尔会破坏一些内联 JS，如果发现某些交互不正常，可以先去掉 `--minify` 排查。

## 香港 Nginx 反代配置

这是为了让国内读者能正常访问。我买了一台香港轻量云服务器，配置不高（1核1G），但用来做静态文件反代绰绰有余。

Nginx 配置如下：

```nginx
server {
    listen 80;
    server_name blog.aibestapp.top;

    location / {
        proxy_pass https://makismkuo.github.io;
        proxy_set_header Host makismkuo.github.io;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # 缓存静态资源
        location ~* \.(jpg|jpeg|png|gif|ico|css|js|woff2?|ttf|svg|eot)$ {
            proxy_pass https://makismkuo.github.io;
            expires 30d;
            add_header Cache-Control "public, immutable";
        }
    }
}
```

关键点：`proxy_set_header Host` 必须设成 GitHub Pages 的原始域名，否则 GitHub Pages 返回 404。因为 GitHub Pages 是根据 Host header 来路由请求的。

缓存策略上，我对图片、字体、CSS 和 JS 设置了 30 天的强缓存。博客的内容类页面不做缓存，方便内容更新后读者立即看到最新版本。

## 踩坑实录

搭建过程中遇到几个问题，记录一下：

### 1. baseURL 填错导致 RSS 链接失效

一开始我把 baseURL 填成了自定义域名 `https://blog.aibestapp.top`，结果 PaperMod 生成的 RSS feed 里的链接全部变成了 `blog.aibestapp.top`。如果读者通过反代访问 RSS，链接是解析正确的；但如果海外读者直接访问 GitHub Pages 的 RSS，链接指向的域名解析不到 GitHub Pages 上，就报错了。后来改成 GitHub Pages 的原生地址才修好。

### 2. Git submodule 导致 Actions 构建失败

第一次配置 workflow 时，我没有在 checkout 步骤加 `submodules: recursive`，结果 Actions 拉下来的是一个空的主题目录，构建直接报错。这个错误信息还不太直观，Hugo 报的是 "failed to resolve page from site config"，一开始我还以为是配置文件写错了，排查了好一阵才发现是主题没有拉下来。

### 3. 搜索页面不显示

PaperMod 的搜索功能需要同时做三件事：配置文件里 `search: true`，`outputs` 里加了 JSON，content 目录下创建了 search.md。我一开始只配了前两项，以为第三项是自动生成的，结果搜索图标一直没出来。翻文档才发现需要手动创建页面。

### 4. GitHub Pages 自定义域名与 CNAME 文件

如果你用 GitHub Pages 绑了自定义域名，GitHub 会在仓库根目录自动生成一个 CNAME 文件。但如果你每次构建都用 `hugo` 重新生成 public 目录，而 CNAME 文件在构建后被覆盖了，域名绑定就会失效。PaperMod 提供了解决方案：在 `static` 目录下放一个 `CNAME` 文件，Hugo 构建时会自动把它拷贝到 public 根目录。或者像我一样干脆不绑自定义域名，用反代解决访问问题。

## 日常写作流程

现在每次写博客的流程非常简洁：

```bash
# 创建新文章
hugo new posts/article-name.md

# 用 VS Code 编辑
code content/posts/article-name.md

# 本地预览
hugo server -D

# 确认无误后推送
git add .
git commit -m "新文章：article-name"
git push
```

push 之后等大约 30 秒，GitHub Actions 构建完成，文章就同时上线到两个入口了。国内读者访问 `blog.aibestapp.top` 走香港反代，海外读者直接访问 GitHub Pages，两边互不影响。

整个搭建过程从零到跑通，包括调研和踩坑，大概花了一下午。如果是熟悉 Hugo 的朋友，照着这篇配置，应该一小时内能搞定。

有什么问题欢迎在评论区留言，我会尽量回复。如果你有自己的博客搭建经验或更好的方案，也欢迎交流。

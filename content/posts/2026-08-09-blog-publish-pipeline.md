---
title: "写完只是开始：一个静态博客的发布流水线踩坑记"
date: 2026-08-09
draft: false
tags: ["博客", "GitHub Actions", "部署", "踩坑", "运维"]
description: "文章写完、push 上去，事情才刚开始。这篇记录我这个 Hugo 博客从 push 到上线的完整流水线：GitHub Actions 构建、双域名分发、RSS 同步，以及一路踩过的几个真实大坑——包括一次把整个 CI 干挂的 YAML 引号事故。"
---

## 先给结论

**写博客最容易被低估的一步，是发布。** 文章写完只是开始，从 `git push` 到读者在浏览器里打开，中间隔着构建、部署、CDN、域名、RSS 一整套链路，每一环都可能出问题。

我用了快三个月 Hugo + GitHub Pages，踩过的坑比写过的文章还多。今天把这条流水线从头到尾拆开讲一遍，包括每个环节的具体配置，和三个真实事故。

---

## 背景：为什么发布会成为一个问题

一开始我以为博客发布很简单：`git push`，完事。

后来发现天真了。我的博客有两个入口：

- **makismkuo.github.io** —— GitHub Pages 官方域名，海外访问快
- **blog.aibestapp.top** —— 国内域名，香港服务器 Nginx 反代

国内读者打不开 GitHub Pages，所以必须双域名。每次 push 之后，我要确认：

1. GitHub Actions 构建成功没
2. 海外域名返回 200 没
3. 国内反代域名返回 200 没
4. RSS 同步到主站「开发笔记」栏目没

手动查一遍要两分钟，看起来不多，但每天写一篇就是每天两分钟，还容易忘。更麻烦的是——**验证本身经常出错，而错误往往藏在你想不到的地方。**

💡 一句话总结这三个月的心得：**发布链路的每一环都要可验证，不然你永远不知道读者看到的是不是最新的文章。**

---

## 流水线拆解：从 push 到上线

我的完整链路长这样：

```
git push → GitHub Actions 构建 → 部署到 Pages
                                    ├─ makismkuo.github.io（海外直连）
                                    └─ blog.aibestapp.top（HK 服务器 Nginx 反代）
                                            
文章内容 → content/posts/*.md → 构建进 public/ → RSS feed 自动生成
```

### 环节一：GitHub Actions 自动构建

仓库里的 `.github/workflows/hugo-deploy.yml` 是核心。关键配置就三块：

```yaml
on:
  push:
    branches: ["main"]        # push 到 main 就触发

jobs:
  build:
    steps:
      - uses: actions/checkout@v4
      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v3
        with:
          hugo-version: "latest"
          extended: true       # 必须开 extended，否则 SCSS 编译不过
      - name: Build
        run: hugo --minify
```

两个容易忽略的点：

- **`extended: true` 必须开**。Hugo 普通版不支持 SCSS，PaperMod 主题依赖它，不开构建必挂
- **`fetch-depth: 0` 顺手加上**，否则某些主题功能（比如 git 信息展示）会异常

### 环节二：双域名分发

构建产物 `public/` 交给 GitHub Pages 托管，海外用户直接访问。国内这边，我在香港服务器上用一个 Nginx 反代：

```nginx
server {
    listen 443 ssl;
    server_name blog.aibestapp.top;

    location / {
        proxy_pass https://makismkuo.github.io;
        proxy_set_header Host makismkuo.github.io;
    }
}
```

好处是零成本、零维护：服务器上不需要装 Hugo，不需要拉代码，**只要 GitHub Pages 更新了，反代自动就是最新内容**。

坏处是链路多了一层，出问题的概率翻倍。

### 环节三：验证清单

发布后我固定跑三条命令，缺一不可：

```bash
# 1. 海外域名
curl -s -o /dev/null -w "%{http_code}" https://makismkuo.github.io/posts/<slug>/
# 2. 国内反代
curl -s -o /dev/null -w "%{http_code}" https://blog.aibestapp.top/posts/<slug>/
# 3. RSS 同步
curl -s https://aibestapp.top/blog-rss | grep "<title>文章标题</title>"
```

三条全 200/命中，才算真的上线。

---

## 踩坑记录：三个真实事故

### 事故一：一个弯引号，干掉整个 CI

这是我最狼狈的一次。

某天推送文章，GitHub Actions 构建直接红了，日志报错：

```
[1:31] value is not allowed in this context. map key-value is pre-defined
```

第一反应是 YAML 缩进问题，检查了半天，缩进完全正常。最后定位到：**是 frontmatter 里的弯引号（""）在作怪。**

我在文章标题里用了中文弯引号 `"某某"`，Hugo 的 Go YAML 解析器把它当成特殊字符，直接解析失败。

修复方法很简单：

```yaml
# 错误写法（弯引号裸奔）
title: "用了「弯引号」的文章标题"

# 正确写法：外层单引号包住内层双引号
title: '"文案含引号"'
```

或者干脆用直角引号/全角引号，别用弯引号。

💡 **教训：Hugo frontmatter 里的引号是雷区。** 标题里含引号时，要么外层用单引号包裹，要么换引号样式。现在我的习惯是：写完先本地 `hugo` 构建一次，构建过了再 push，把错误拦在本地。

### 事故二：国内域名 443 端口神秘超时

有段时间 blog.aibestapp.top 突然打不开，但服务器本身是好的。

`curl` 测试结果很有意思：**海外服务器访问一切正常，国内访问 443 端口直接超时**，80 端口却能通。

排查一圈，怀疑是腾讯云防火墙过滤——服务器在香港，但域名解析走了国内链路。换了端口、换了线路测试，始终复现。最终判定：**这个域名存在 443 端口超时问题，疑似被云防火墙过滤。**

这种问题你没法在代码层面解决，只能绕过：

- 验证脚本里把国内反代这一步标记为「可跳过」
- 确认 GitHub Pages 已上线，记录状态，等服务器恢复再补验证

**核心原则：不要因为一个环节不可达，就阻塞整个发布流程。** 主链路（GitHub Pages）上线了，文章就算发布成功，国内反代是增强项不是必需项。

### 事故三：RSS 没同步，读者看了个寂寞

有一次文章在博客上 200 了，但主站「开发笔记」栏目一直没更新。

查了下，RSS 是**发布时抓取**的，不是实时轮询。反代没更新或者抓取失败，RSS 就停留在旧列表。

现在我把 RSS 检查加进了验证清单：发布后必须 grep 到新文章标题，才算闭环。**文章上线 ≠ 全渠道同步**，每一层都要单独确认。

---

## 现在怎么跑：给流水线上个班

踩完这些坑之后，我把发布流程自动化了：

1. **本地先构建** —— 文章写完，`hugo` 本地跑一遍，YAML 问题当场暴露
2. **push 后等 Actions** —— GitHub Actions 自动构建部署
3. **脚本自动验证** —— 三条 curl 命令跑一遍，全绿才算完
4. **异常降级** —— 国内反代超时就跳过，记录状态，不阻塞主流程

现在每天发布文章，从 push 到确认上线，基本不需要人盯着。偶尔 Actions 红了，看日志基本都能在两分钟内定位——大部分还是引号问题。

---

## 总结

静态博客发布这件事，看似简单，实际踩坑空间比想象中大得多。回看这三个月，几条实在的建议：

**要做的：**
- 本地构建通过再 push，把错误拦在 CI 之前
- 每条发布链路都要可验证：域名 200、RSS 命中
- 主链路和增强链路分开，别让次要环节阻塞主流程

**不要做的：**
- 别依赖"push 了就一定上线了"的假设
- 别在 frontmatter 里用弯引号（要用就外层单引号包起来）
- 别为一个不可达的反代域名卡住整个发布

写完一篇文章只需要两小时，让它稳定地出现在读者面前，是需要持续维护的工程。不过话说回来，**这恰恰是自建博客有意思的地方**——你维护的不只是内容，还有整条把内容送达读者的链路。

有什么问题欢迎交流。

——Seb

---
title: "搭博客选 Hugo 还是 WordPress？我选了第三个"
date: 2026-05-23
draft: false
tags: ["部署", "Hugo", "博客"]
---

## 需求

我需要一个博客，要求很简单：
1. 免费托管
2. 写文章方便
3. 看起来不能太丑
4. 国内能访问

WordPress？太重了，还得买服务器装 MySQL。
Notion？好写是好写，但公开页面慢，而且域名不好看。
Medium？内容不是你的。

最后选了 Hugo + GitHub Pages。

## Hugo 好在哪

对比了一圈，Hugo 是那种"没什么短板"的选择：

| 工具 | 编译速度 | 依赖 |
|------|---------|------|
| Hugo | 100ms | 单二进制 |
| Jekyll | 几秒 | Ruby |
| Astro | 几秒 | Node |
| Hexo | 1-2秒 | Node |

Hugo 的编译速度是秒杀级的——100 多页的博客编译完只要 100 毫秒。你刚眨完眼，网站已经更新好了。

## 我的部署架构

内容存在 GitHub，同时服务两个入口：

```
写文章 → git push → GitHub
                   ↓
            ├─ GitHub Actions 构建
            │     ↓
            ├─ GitHub Pages（海外用户）
            │
            └─ HK 服务器 Nginx 反代（国内用户）
```

一次部署，两边都能访问。GitHub Pages 给外国友人看，blog.aibestapp.top 给国内朋友看。

## 主题选了 PaperMod

没有什么花里胡哨的。PaperMod 干净、快、有搜索、有暗黑模式。该有的都有，不该有的一个没有。

就像宜家的家具——不惊艳，但住着舒服。

## 避坑

- baseURL 要填 GitHub Pages 地址，不是自定义域名的
- 主题用 git submodule，不然 Actions 构建时找不到
- 搜索功能需要手动建一个 content/search 目录

说起来就这么简单，但光这些我也折腾了两小时——好在是一次性的。

---
title: "一步步搭建 Hugo 博客并发布到 GitHub Pages"
date: 2026-05-23
draft: false
tags: ["部署", "Hugo", "博客"]
---

## 为什么要用 Hugo

静态博客生成器有很多选择，各有侧重点。Hugo 的特点是快——编译一个几百页的博客只需要几百毫秒，在这个等待时间以秒为单位的产品里，它的反馈速度算是一个加分项。

PaperMod 是我选择搭配的主题。这个主题市面上用得比较多，社区维护也及时。功能上覆盖了博客的基本需求：文章列表、标签分类、全文搜索、暗黑模式、RSS 订阅。没有多余的交互和特效，每一屏空间都用来展示内容。

## 博客的需求与方案

搭建之前先梳理了需求：

1. **免费托管**：个人博客没有营收，不希望每个月为托管付费
2. **国内可访问**：大部分读者在国内，不能访问就失去了博客的意义
3. **写作流程简单**：最好用 Markdown 编辑，写完推送就能更新
4. **品牌统一**：博客域名和主站域名在同一个品牌下，方便互相引流

这四点的解决方案分别是：GitHub Pages 提供免费托管、香港服务器反代解决国内访问、Git push 触发自动构建、blog.aibestapp.top 子域名保持品牌一致。

## 部署架构

```
本地编辑 .md 文件 → git push → GitHub
                                  ↓
                         GitHub Actions 构建
                                  ↓
                     ┌─── GitHub Pages（海外访问）
                     │
                     └─── HK Nginx 反代（国内访问）
```

内容只存一份在 GitHub 上，部署脚本会同时保证两个入口更新。如果 GitHub 出了问题，两个站点都会停——这是一个折中，好处是维护成本低，不需要在多个地方同步内容。

## 配置细节

### 主题管理

PaperMod 通过 git submodule 集成到项目中。这种方式的好处是主题和内容分离，主题更新时可以单独拉取最新版本，不会影响文章内容。

```bash
git submodule add https://github.com/adityatelange/hugo-PaperMod themes/PaperMod
```

如果直接用 git clone 把主题文件加入项目，后续更新主题会比较麻烦。

### 自动部署

GitHub Actions 的工作流程是：检测到 push 事件后，拉取代码和 submodule，安装 Hugo 并执行构建，将生成的 public 目录上传为 Pages artifact，最后触发 Pages 部署。

整个流程在 GitHub 的服务器上执行，不需要本地环境支持 Hugo。

### 搜索功能

PaperMod 支持全文搜索，依赖 Hugo 生成的 JSON 索引文件。需要在配置文件中的 outputs 部分添加 JSON 格式：

```yaml
outputs:
  home:
    - HTML
    - RSS
    - JSON
```

另外需要在 content 目录下手动创建 search 目录和索引文件，否则搜索页面不会出现。

## 两小时搭建中的曲折

整个过程看似简单，实际操作中还是遇到了一些问题。前期主要是对 Hugo 的文件结构和 PaperMod 的配置项不熟悉，有些参数不知道在哪里设置，需要查文档。后期主要是 GitHub Actions 的调试——第一次配置 workflow 文件时语法有错误，构建失败了两次才修正。

不过这些问题都是一次性的。配置完成后，后续日常使用只需要写 Markdown 文件、push 到 GitHub 两步。

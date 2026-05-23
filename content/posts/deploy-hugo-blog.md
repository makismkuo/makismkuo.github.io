---
title: "用 Hugo + PaperMod 搭一个技术博客"
date: 2026-05-23
draft: false
tags: ["部署", "Hugo", "GitHub", "博客"]
---

## 为什么选 Hugo

对比主流静态博客生成器：

| 工具 | 速度 | 依赖 | 学习曲线 |
|------|------|------|---------|
| Hugo | 极快 | 单二进制 | 低 |
| Jekyll | 慢 | Ruby | 中 |
| Astro | 中等 | Node.js | 中高 |
| Hexo | 中等 | Node.js | 低 |

Hugo 编译一个博客只要 100ms，主题 PaperMod 简洁够用。

## 架构

```
本地编辑 .md 文件
       │
       ├─ git push → GitHub
       │
       ├─ GitHub Actions 构建 → GitHub Pages（海外访问）
       │
       └─ HK Nginx 反代 → blog.aibestapp.top（国内访问）
```

## 自动化配置

- 推送到 `main` 分支 → 自动构建部署
- PaperMod 自带搜索、暗黑模式、目录、代码复制
- 支持 RSS 订阅，方便后续跨站同步

## 避坑

- `hugo.yaml` 里 `baseURL` 要填 GitHub Pages 的地址
- 主题用 `git submodule` 管理，否则 Actions 构建找不到
- PaperMod 的 search 页面需要手动创建 `content/search/_index.md`

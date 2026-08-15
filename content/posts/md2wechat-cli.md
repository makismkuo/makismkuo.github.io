---
title: "md2wechat：把 Markdown 一键变成公众号文章的 CLI"
date: 2026-08-15
draft: false
tags: ["开源", "推荐", "GitHub", "CLI", "AI"]
---

写公众号的人大多经历过这种痛苦：Markdown 里排版好好的，一粘进微信编辑器，代码块碎了、引用变灰、图片全丢，最后只能花半小时手工调格式。写内容只花 10 分钟，排版反而花 30 分钟，本末倒置。

**md2wechat** 就是来终结这件事的。一个面向 AI Agent 的微信公众号创作与发布 CLI：写 Markdown，它帮你生成公众号排版、做封面和配图、预览校验后直接推送到草稿箱。目前已 3500+ star，仍在活跃更新。

## 它是做什么的

md2wechat 把公众号发布流程拆成一组可验证的 CLI 命令：`convert` 负责 Markdown 转微信 HTML，支持预览、上传图片、创建草稿；`inspect` 在发布前检查标题、摘要、图片、封面和草稿就绪状态；`capabilities`、`doctor`、`themes` 等 discovery 命令则是给 Agent 用的可机读接口。

它面向的正是 AI 工作流：支持 Claude Code、Codex、Kimi Work，连 Hermes Agent 也在列表里。写文章、排版、配图、发草稿，全链路可以让 Agent 自动完成。

## 核心功能

- **40+ 排版样式和专业主题**：API 模式下有 48 个微信渲染精调主题，还有 68 个高级排版场景条目、53 个 `:::` 语法模块，代码块、引用、卡片都能正常渲染。
- **AI 配图与封面**：内置 `generate_cover`、`generate_infographic`，内容生产命令还包括 `write`、`humanize`、`title suggest`。
- **多账号管理**：支持命名公众号账号，本地只读发现凭证，不输出 Secret。
- **发布前检查**：`inspect --json` 输出标题、摘要、图片、封面、草稿就绪状态，避免"发出去了才发现封面没设"。
- **Agent 友好**：全部命令支持 `--json` 输出，还有 `doctor` 自检，机器可读、可稳定调用。

## 为什么值得关注

公众号排版是个又脏又累的活，但恰恰是 AI 最适合干的活——规则明确、重复度高、试错成本低。md2wechat 的价值在于它把"排版美化"这种主观的事情，拆成了确定性命令：输入 Markdown，输出可直接发布的微信 HTML。加上 `inspect` 的发布前检查，等于给 Agent 加了一道安全阀，让自动化发布不再靠运气。

对个人开发者来说，这意味着"写博客 → 同步发公众号"可以完全自动化：Markdown 写一次，网页和公众号同时出稿。对做矩阵号、客户号的内容团队，批量发布和多账号管理更是刚需。

## 快速上手

```bash
npm install -g @geekjourneyx/md2wechat
md2wechat config init --json   # 配置微信凭证
md2wechat inspect article.md --json              # 发布前检查
md2wechat convert article.md --output article.html
md2wechat convert article.md --draft --cover cover.jpg  # 建草稿
```

## 总结

md2wechat 解决的问题很具体：公众号排版不该是内容创作里最耗时的环节。它把 Markdown 到微信文章的全流程变成一组确定性 CLI 命令，既适合人手动用，也适合接进 AI Agent 自动跑。如果你在写公众号、或者准备让 Agent 帮你发文章，值得装上试试——排版这件破事，以后真的可以不用亲手干了。

项目地址：[github.com/geekjourneyx/md2wechat-skill](https://github.com/geekjourneyx/md2wechat-skill)

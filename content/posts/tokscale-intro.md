---
title: "Tokscale：一个 TUI 盯死你所有 AI 编码代理的 token 消耗"
date: 2026-06-14
draft: false
tags: ["开源", "推荐", "GitHub", "AI", "CLI"]
---

如果你同时在用 Claude Code、Codex CLI、Gemini CLI、OpenCode 这些 AI 编码工具，有没有想过一个问题——**这些代理一个月到底吃掉了我多少 token？**

每个工具各自统计各自的，互不通气。月底看到账单才傻眼。如果能有一个仪表盘，把所有代理的 token 用量、花费、速率限制一屏看完，心里就有底了。

**Tokscale** 就是干这个的。

## Tokscale 是什么

Tokscale 是一个 Rust 编写的 TUI 工具，定位是"AI 编码代理的 token 用量监控仪表盘"。它追踪你所有 AI 编码工具的 token 消耗和费用，并把数据汇总到一个统一的本地排行榜里。

项目地址：[github.com/junhoyeo/tokscale](https://github.com/junhoyeo/tokscale)，目前 3700+ Star，MIT 协议，Rust 编写，跨平台（macOS/Linux/Windows）。

## 核心功能

Tokscale 的覆盖范围很广，目前支持 Claude Code、Codex CLI、Gemini CLI、Cursor、OpenCode、OpenClaw、Factory Droid、Pi、AmpCode、Kimi 等主流 AI 编码代理。它会自动检测这些工具的 token 使用记录，不需要手动配置。

展示的信息包括：

- **实时 token 用量**：每个代理当前 session 的 input/output token 计数
- **费用统计**：按代理类型和模型汇总的累计花费，支持美元和韩元
- **全局排行榜**：看哪个代理最"烧钱"，哪个最省，榜一榜二一目了然
- **历史趋势**：按天/周展示 token 消耗变化曲线，发现异常激增
- **速率限制状态**：当前 API 调用余量，避免触发限流
- **贡献图**：2D/3D 的贡献热力图，像 GitHub 绿格子一样展示你的 AI 编码活跃度

数据完全本地存储，不做任何网络请求，不需要额外 API Key。

## 为什么值得关注

### 多代理时代的刚需

AI 编码代理正在爆发，每个代理都有自己的 token 统计方式。有的数据藏在日志文件里，有的通过 API 回传，有的根本不提供。你用 3-4 个代理工作一周就彻底失去对 token 的控制。Tokscale 把一个本应很麻烦的问题——**碎片化的 token 数据整合**——做成了一个开箱即用的工具。

### Rust 性能，原生 TUI

用 Rust 写意味着启动和刷新几乎无感。原生 TUI 交互流畅，`↑`/`↓` 导航、排行榜排序、切换视图，响应都在毫秒级。对于本就天天泡在终端里的开发者来说，这个体验远比开个网页看 dashboard 舒服。

### 竞争动机：全球排行榜

Tokscale 还有一个有趣的全球排行榜功能——你可以看到所有用户的总 token 消耗排名。虽然本质上是"看谁给 AI 交的钱多"，但确实增加了点好胜心。开源社区的参与度也因此很高。

## 安装和使用

安装非常简单，一行命令：

```bash
curl --proto '=https' --tlsv1.2 -LsSf https://github.com/junhoyeo/tokscale/releases/latest/download/tokscale-installer.sh | sh
```

或者用 Cargo 从源码编译：

```bash
cargo install tokscale
```

使用上几乎没有学习成本：

```bash
tokscale          # 启动 TUI 仪表盘
tokscale --once   # 打印当前 token 快照后退出（适合脚本集成）
```

在 TUI 界面中，`↑`/`↓` 切换代理，排序视图可以按 token 总量、费用、session 时长等维度排列。配置项写在 `~/.config/tokscale/config.toml`，可以指定你想监控的代理类型，或者隐藏不用的。

## 和类似工具的对比

| 工具 | 定位 | 关注点 | 星数 |
|------|------|--------|------|
| Tokscale | AI 代理 token 监控仪表盘 | 所有代理的 token/费用汇总 | ~3700 |
| abtop | AI 代理任务管理器 | 代理进程状态（context/端口） | ~2500 |
| agent-deck | AI 代理 session 管理器 | 多 session 切换和管理 | ~2600 |

abtop 侧重"代理们在干嘛"，而 Tokscale 侧重"代理们花了多少钱"。两者不冲突，可以同时用——abtop 看工作状态，Tokscale 看成本。

## 结语

Tokscale 解决的是一个从"一个人用一两款 AI 编码工具"到"一个人同时用五六款 AI 编码工具"这个演进过程中自然产生的问题。当 AI 编码代理成为开发者的标配工具箱，token 用量监控就不是锦上添花，而是刚需。

如果你已经习惯使用多个 AI 编码代理，或者正准备把 AI 编码工具融入日常开发流，装一个 Tokscale 花不了两分钟。它能让你对 AI 的使用成本始终保持清晰认知——**看得见的数字，就是管得住的成本**。

项目地址：[github.com/junhoyeo/tokscale](https://github.com/junhoyeo/tokscale)

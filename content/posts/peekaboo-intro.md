---
title: "Peekaboo：让AI真正"看见"你的Mac屏幕"
date: 2026-06-20
draft: false
tags: ["开源", "推荐", "GitHub", "macOS", "AI工具"]
description: "Peekaboo 是 macOS 上的一款开源 CLI + MCP 服务器，让 AI 代理能截屏、分析画面、点击按钮、输入文字 —— 真正的屏幕级自动化，一句话搞定。"
---

如果你用过 Claude 的 Computer Use 或类似的 AI 代理工具，一定遇到过这个问题：**AI 能思考，但看不见你的屏幕**。它只能猜你的环境长什么样，没法真正"看一眼"。

[Peekaboo](https://github.com/openclaw/Peekaboo)（⭐ 4.7k）就是来解决这个的。它是一个 macOS 原生工具，让 AI 代理（Claude Code、Codex、Cursor、任何 MCP 客户端）能截屏、分析画面、识别元素、点击按钮——整个过程在后台完成，不抢你的鼠标键盘焦点。

### 核心功能

一句话：**AI 能像人一样操作你的 Mac，但更快、更可控**。

具体能力清单有点长，但每个都很实用：

- **像素级截图**：窗口、全屏、菜单栏，支持 Retina 2x 缩放
- **UI 元素识别 + 操作**：截屏后给 AI 返回带元素 ID 的快照，AI 可以直接说"点那个按钮"——`peekaboo click --on "Reload this page" --snapshot xxx`
- **后台操作**：默认不激活目标 App，Safari 在后台被操控，你在前台写代码
- **自然语言代理**：`peekaboo agent "打开备忘录，创建三个待办事项"`——一条命令走完
- **MCP 服务器**：一行 `npx -y @steipete/peekaboo` 就能接入任何 MCP 客户端
- **多屏支持**：不只有主屏，多显示器场景也能覆盖
- **多 AI 模型**：支持 OpenAI、Anthropic、Ollama、LM Studio 等，本地模型也行

安装只有一行：`brew install steipete/tap/peekaboo`。

### 为什么值得关注

Peekaboo 不是那种"理论上很酷"的项目。它的命令都是可执行的，我实际试过——用它自动填表单、截 Debug 日志、点确认弹窗，都能跑通。

几个让我觉得它特别的地方：

1. **后台操作不抢焦点**。默认所有鼠标/键盘事件都发往目标进程，不激活窗口。你可以一边写代码，一边让 AI 帮你操作浏览器填表格。
2. **MCP 原生集成**。在 Claude Code 或 Cursor 的 MCP 配置里加上 Peekaboo，AI 就能自动截屏、看图操作。这意味着你不再需要"描述当前界面给 AI"，它自己看。
3. **Permission 处理完善**。macOS 的 Screen Recording 和 Accessibility 权限向来麻烦，Peekaboo 有专门的权限检查和引导命令（`peekaboo permissions grant`），不用折腾系统设置。
4. **Mac 原生（Swift）**。不是 Electron 套壳，性能好，启动快。

### 简单示例

安装后，截个全屏看看：

```bash
# 截屏并保存到桌面
peekaboo image --mode screen --retina --path ~/Desktop/my-screen.png

# 让 AI 帮你操作 Safari（需要 MCP 配置）
peekaboo agent "打开 Safari，访问 github.com/trending，截图保存"
```

在 Claude Code 中接入 MCP：

```json
{
  "mcpServers": {
    "peekaboo": {
      "command": "npx",
      "args": ["-y", "@steipete/peekaboo"]
    }
  }
}
```

配置好后，你的 AI 编码代理就能直接控制浏览器、终端、备忘录——任何 Mac 上的应用。

### 总结

Peekaboo 把"AI 看屏幕"这件事从实验室级别变成了开发者日常可用。它开源、MIT 协议、macOS 原生、MCP 天然兼容，在 AI 自动化工具链里是不可或缺的一块拼图。

如果你在用 Claude Code、Codex 或 Cursor 做编码代理，装一个 Peekaboo 就能突破"AI 看不见"这个瓶颈，大幅提升自动化的覆盖范围。

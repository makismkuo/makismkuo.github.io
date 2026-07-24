---
title: "xplr：一个可hack的极速终端文件浏览器"
date: 2026-07-24T09:00:00+08:00
draft: false
tags: ["开源", "推荐", "GitHub", "CLI", "Rust", "效率工具"]
description: "xplr：轻量、快速、Lua可编程的终端文件浏览器，让文件操作如行云流水"
---

## xplr：终端文件浏览的"乐高"

在终端里操作文件，多数人的选择无非是 `cd` + `ls` 反复敲，或者装一个 ranger / lf 之类的 TUI 管理器。但如果我说有一个项目，既保留了终端的极速体验，又把 **"可 hack 性"** 做到了极致——它就是 [xplr](https://github.com/sayanarijit/xplr)（⭐4785，纯 Rust 编写）。

xplr 的定位很特别：它**不是**传统意义上"开箱即用"的文件管理器。它更像是一个画布，你用 Lua 脚本 + 键绑定 + 管道组合出自己**理想中的**文件操作流程。

## 核心功能

作为一个终端文件浏览器，xplr 把基本功打得很扎实：

- **极速渲染**：Rust 编写，打开再大的目录也不卡
- **全键盘操作**：vim 风格快捷键，手不离键
- **可编程布局**：文件列表、预览面板、面包屑——位置和内容全由你控制
- **Lua 脚本扩展**：按键映射、管道、批量操作、自定义排序，全通过 Lua 脚本实现
- **插件生态**：[awesome-plugins](https://xplr.dev/en/awesome-plugins) 集合了社区贡献的几十个插件
- **集成万物**：可以与 fd、ripgrep、fzf、bat、zoxide 等几乎所有 CLI 神器无缝对接

这些功能单独拎出来都不稀奇，但 xplr 的独特之处在于——**所有行为都可以被改写**。觉得默认的预览方式不够好？写十几行 Lua 换成你想要的。想一键搜索某目录下的 Python 文件再批量替换？绑定一个快捷键，xplr 自动 pipe 到 rg + sed。

## 为什么值得关注

在 "bloat is feature" 的时代，xplr 选择了相反的路线——**最小内核 + 最大可塑性**。这种设计哲学有几个实实在在的好处：

1. **你不是被工具塑造，而是你塑造工具**。很多终端文件管理器用习惯后，换不得；而 xplr 的配置本身就是可分享的 dotfile，一份配置带你到任何机器。
2. **贴合真实工作流**。不是"请用我的方式浏览"，而是"告诉我你想怎么浏览"。xplr 的插件和集成文档里有一堆让人拍大腿的实战案例——比如用 xplr 当模糊搜索启动器、批量重命名工具、批量 git add 预览器。
3. **Rust 基层保证性能**。同样复杂的操作，xplr 的渲染速度明显比 Python 写的同类工具快，在 WSL 和树莓派上尤其明显。

## 一句话示例

```bash
# 安装（macOS）
brew install xplr

# 启动
xplr

# 基本操作
j/k   : 上下移动
l     : 进入目录 / 打开文件
h     : 返回上级
space : 选中/取消选中
g     : 跳转到
~     : 跳转到 home
/     : 过滤文件名
```

如果要让它更强大，写一个简单的 Lua 配置来集成 fd + fzf + bat：

```lua
-- ~/.config/xplr/init.lua
xplr.config.modes.builtin.default.key_bindings["F"] = {
  help = "fuzzy find files",
  messages = {
    "BashExec@fd --type f | fzf --preview 'bat {}' | while read f; do xplr --switch $f; done"
  }
}
```

按 `F` 键即可全目录模糊搜索，选中后 xplr 直接定位到该文件。

## 总结

xplr 适合**喜欢折腾终端、追求极致效率、不想被工具框死**的开发者。它不是为"随便用用"的人准备的——它是为那些愿意花 30 分钟配置、换来未来数百小时效率提升的人准备的。

如果你日常工作流中频繁接触文件系统，xplr 值得一试。GitHub ⭐4785，活跃维护，文档优美，社区插件丰富。复制粘贴十条命令可能让你对文件管理改观。

> **GitHub**: [github.com/sayanarijit/xplr](https://github.com/sayanarijit/xplr)
> **文档**: [xplr.dev](https://xplr.dev/en)

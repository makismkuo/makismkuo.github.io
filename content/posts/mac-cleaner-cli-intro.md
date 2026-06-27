---
title: "mac-cleaner-cli：免费开源的 CleanMyMac 替代品，一行命令清掉几十 GB"
date: 2026-06-27
draft: false
tags: ["开源", "推荐", "GitHub", "CLI", "macOS"]
---

你的 Mac 硬盘是不是又黄了？几百 MB 的 Xcode DerivedData、Homebrew 下载缓存、Docker 僵尸镜像、浏览器缓存——每个几十到几百 MB，日积月累就是几十 GB，而且还散布在系统各个角落，手动清理不现实。

CleanMyMac X 要 $39.95/年，DaisyDisk 要 $9.99。花钱买清理工具总觉得有点亏。开源的替代方案来了。

## mac-cleaner-cli 是什么

**mac-cleaner-cli** 是一个终端 CLI 工具，专门扫描和清理 macOS 上的垃圾文件。Node.js/TypeScript 编写，一行命令启动，交互式选择要删的内容，100% 离线运行，不联网、不上传、不装守护进程。

项目地址：[github.com/guhcostan/mac-cleaner-cli](https://github.com/guhcostan/mac-cleaner-cli)，目前 1,800+ Star，MIT 协议。

## 核心功能

它把可清理的项分成三个安全等级：

**🟢 安全级**——Trash、临时文件、浏览器缓存（Chrome/Safari/Firefox/Arc）、Homebrew 下载缓存、Docker 无用镜像。这些随便删，不会出问题。

**🟡 中等安全**——系统日志、开发缓存（npm/yarn/pip/Xcode DerivedData/CocoaPods）、废弃项目的 node_modules。一般安全，但极端情况可能要用到某些缓存重编译。

**🔴 高风险**（需加 `--risky` 标志）——30 天前的 Downloads、iOS 备份、邮件附件、重复文件、500MB+ 的大文件、未使用的语言包。这些需要你确认后再删。

使用方式非常简单：

```bash
# 不用安装，直接跑
npx mac-cleaner-cli

# 含高风险项目
npx mac-cleaner-cli --risky
```

它会先扫描，列出各类目和预估释放空间，用空格勾选要清理的项，回车确认，一步到位。

还附带一些实用子命令：

- `npx mac-cleaner-cli uninstall` — 扫描并彻底卸载应用，带走偏好设置和缓存
- `npx mac-cleaner-cli maintenance --dns` — 刷新 DNS 缓存
- `npx mac-cleaner-cli maintenance --purgeable` — 释放可清除空间
- `npx mac-cleaner-cli categories` — 列出所有支持清理的类目

高级功能包括文件夹级选择——在交互界面按 `→` 展开目录树，进到子目录精确选择要删的文件，而不是清空整个缓存文件夹。

## 为什么值得关注

**痛点精准**——macOS 用户没有不知道硬盘吃紧的。每次系统提示"磁盘空间不足"都让人烦躁。mac-cleaner-cli 精确地切了这个场景，而且做得比预想的好。

**安全设计用心**——不是一把梭全删。按风险分三级，高风险默认隐藏，需要用户主动加 `--risky` 才展示。支持文件级选择，不是粗暴地 `rm -rf ~/Library/Caches`。删除前有备份机制，可以回滚。

**完胜付费工具**——CleanMyMac X 一年 $40 还是订阅制，mac-cleaner-cli 免费开源，功能覆盖了 90% 的日常清理需求。不跑后台进程，不收集任何数据，用完即走，没有弹窗提醒你"该续费了"。

**原生支持 Homebrew/Xcode**——这是 macOS 开发者最头疼的硬盘杀手。Homebrew 的下载缓存（`~/Library/Caches/Homebrew`）动辄几个 GB，Xcode DerivedData 和旧 iOS Simulator 也是磁盘大户。mac-cleaner-cli 原生支持扫描这些开发者专属的垃圾文件，比通用清理工具更懂你的环境。

## 简单示例

```bash
# 1. 扫描并清理
npx mac-cleaner-cli

# 2. 看到扫描结果后，勾选要清理的类目
# 3. 回车确认，完成

# 定期使用的话，装到全局
npm install -g mac-cleaner-cli
mac-cleaner-cli
```

如果你习惯 CI/CD 或想自动化清理流程，`--file-picker` 和 `--absolute-paths` 这些标志也让它在脚本中足够灵活。

## 总结

mac-cleaner-cli 不做什么花哨的事——它就是帮你找到 Mac 上的垃圾文件然后清掉，而已。但它把这件事做得足够好：安全分级、文件级选择、开发者工具缓存专精、交互流畅。对于不想花 $40 买 CleanMyMac、也不想为了清理硬盘翻遍 Finder 的 macOS 用户来说，这是一个零成本的替代方案。

<!-- 想一次性回收几十 GB 又不想花钱？这个就够了。 -->

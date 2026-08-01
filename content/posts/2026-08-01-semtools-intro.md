---
title: "SemTools：终端里的本地语义搜索引擎，给文档装个AI大脑"
date: 2026-08-01
draft: false
tags: ["开源", "推荐", "GitHub", "AI", "CLI"]
description: "SemTools 是 LlamaIndex 官方出品的 CLI 语义搜索工具，把 PDF/DOCX 解析成 Markdown、用多语言向量模型做本地语义搜索，还能用 AI Agent 直接问答你的文档库。"
---

每天面对一堆 PDF、DOCX、论文和 Markdown，想找一句话只能靠 Ctrl+F 逐字匹配；想把文档喂给 LLM 做问答，还得先折腾解析和向量库。**SemTools** 把这些事压成了一个命令：解析、语义搜索、AI 问答，全在终端里完成。

SemTools 是 LlamaIndex 官方团队开源的高性能 CLI 工具（[github.com/run-llama/semtools](https://github.com/run-llama/semtools)，1842 Stars，Rust 编写，MIT 协议），专为命令行文档处理和语义搜索打造，速度与可靠性俱佳。

## 四个子命令，覆盖完整工作流

- **`semtools parse`** — 把 PDF、DOCX、PPTX 等文档解析成干净 Markdown，默认走 LlamaParse 后端，自带缓存和错误处理，支持并发加速
- **`semtools search`** — 本地语义搜索，使用 model2vec 多语言嵌入模型做余弦相似度匹配，可调距离阈值和返回行数，完全离线
- **`semtools ask`** — 带搜索和读取工具的 AI Agent，直接对文档集合提问（默认 OpenAI，可配置任意 OpenAI 兼容 API）
- **`semtools workspace`** — 工作区管理，为大规模文档集合建立索引缓存（支持 IVF_PQ），增删文件自动重嵌入

## 为什么值得关注

首先是**快且离线**：search 和 workspace 完全本地运行，不依赖任何云端服务，隐私敏感文档也能放心处理；底层用 Rust 实现，解析和检索速度远超 Python 同类工具。其次是**管道化设计**：所有子命令都遵循 Unix 哲学，支持 stdin/stdout 衔接——可以 `parse` 完直接 `xargs search`，还能和 grep 组合做精确预过滤，塞进 shell 脚本就是一条完整的文档处理流水线。最后是**出身可靠**：LlamaIndex 官方出品，与 LlamaParse 生态天然打通，API 设计简洁，文档完善。

## 简单示例

```bash
# 安装
npm i -g @llamaindex/semtools

# 解析 PDF 并搜索
semtools parse research_papers/*.pdf | xargs semtools search "API endpoints"

# 直接对文档提问
semtools ask "Summarize the key methodologies" papers/*.txt

# 大文档集用工作区加速
semtools workspace use my-workspace
semtools search "semantic search" ./docs/*.txt --n-lines 5 --top-k 10
```

## 总结

SemTools 把「解析 → 索引 → 检索 → 问答」这条文档处理链路压缩成了四条命令，让语义搜索像 `grep` 一样随手可用。如果你经常和论文、报告、合同打交道，或者想给本地文档库搭一个离线问答入口，它绝对值得一试。唯一的门槛是 parse 需要免费注册 LlamaIndex Cloud Key——但 search 和 workspace 完全免费离线，先装来搜一搜旧文档，立刻就能感受到和 Ctrl+F 的差距。

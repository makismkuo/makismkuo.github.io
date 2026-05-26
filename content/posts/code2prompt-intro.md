---
title: "Code2Prompt：把整个代码库变成 LLM 提示词"
date: 2026-05-26
draft: false
tags: ["开源", "推荐", "GitHub", "AI", "开发工具"]
---

## 一个不算新但很痛的场景

在用 AI 辅助写代码的时候，很多人的做法是：把当前编辑的文件复制粘贴给 ChatGPT/Claude，让模型帮忙分析或修改。

问题是，一个函数改了，可能影响十个文件。只给 AI 看一个文件，它给出的建议往往会忽略全局上下文，出现各种水土不服——用了不存在的变量、调了不对的签名、生成的代码风格跟项目格格不入。

Code2Prompt 就是来解决这个问题的。

它是一个命令行工具，功能一句话就能说清楚：**把整个代码库的结构和内容打包成一个 Markdown 文件，直接喂给 LLM 做分析**。

项目地址：[github.com/raphaelmansuy/code2prompt](https://github.com/raphaelmansuy/code2prompt)，目前 883 个 Star，MIT 协议，纯 Python 实现。

## 核心功能

安装很简单：

```bash
pip install code2prompt
# 或者用 pipx 隔离安装
pipx install code2prompt
```

基本用法：

```bash
# 处理单个文件
code2prompt --path /path/to/your/script.py

# 处理整个项目，输出到文件
code2prompt --path /path/to/your/project --output project_summary.md
```

它会生成一个结构清晰的 Markdown 文件，包含项目的目录树、每个源文件的内容，以及 token 统计：

```bash
code2prompt --path /path/to/your/project --tokens
```

输出结果可以直接复制给 AI，也可以配合 `llm` 命令行工具直接做管道：

```bash
code2prompt --path /path/to/your/project | llm "分析这个项目的架构"
```

这个组合非常实用。

## 为什么值得关注

### 1. 抑制注释，只留逻辑

代码里的注释对 AI 来说往往是噪音。Code2Prompt 提供 `--suppress-comments` 参数，可以自动去掉文件中的注释，让 LLM 只关注实际代码逻辑：

```bash
code2prompt --path /path/to/your/project --suppress-comments
```

对于复用老项目代码或做代码审查的场景，这个功能很实在。

### 2. 灵活的过滤和排除

大项目里不是所有文件都需要喂给 AI。`node_modules`、`dist` 目录、配置文件和日志文件可以自动排除：

```bash
code2prompt --path /path/to/your/project \
  --filter "**.py" \
  --exclude "**/tests/**" \
  --output analysis.md
```

支持 glob 通配符，控制粒度很细。

### 3. 智能 token 管理 + 费用估算

LLM 都有 token 上限。Code2Prompt 不仅能统计 token 数，还能估算在不同模型上的开销：

```bash
code2prompt --path /path/to/your/project --tokens --price --provider openai --model gpt-4
```

这个功能对控制 API 成本很有帮助，尤其当你需要频繁给 AI 喂代码的时候。

### 4. 自定义 Jinja2 模板

内置了几套模板：代码分析、代码审查、生成 README 等。也可以写自己的模板：

```bash
code2prompt --path /path/to/your/project --template my_template.j2
```

甚至支持模板变量输入，在运行时交互式填写信息：

```jinja2
# {{input:project_name}} 代码审查
你的任务是审查以下代码库，重点关注 {{input:focus_area}}
```

### 5. 行号 + 语法高亮映射

生成的代码块带行号，方便跟 AI 讨论具体位置。也可以自定义文件扩展名对应的语法高亮：

```bash
code2prompt --path /path/to/your/project \
  --syntax-map "inc:bash,customext:python" \
  --line-number
```

## 使用示例

### 代码审查

团队做 Code Review 之前，把 PR 涉及的所有代码打包喂给 AI，做一个初步的架构分析和潜在问题扫描：

```bash
code2prompt --path /path/to/pr/files \
  --filter "**.py,**.js" \
  --exclude "**/tests/**" \
  --template code_review.j2 \
  --output pr_review.md
```

### 生成项目文档

打算写项目文档，但不知道从何写起？把代码结构交给 AI，让它自动生成 README 的骨架：

```bash
code2prompt --path /path/to/your/project \
  --template create-readme.j2 \
  --output readme_draft.md
```

### 重构建议

老项目堆了几年代码，想重构又不确定从哪里下手：

```bash
code2prompt --path /path/to/legacy-code \
  --suppress-comments \
  --tokens \
  --line-number \
  | llm "分析这个项目的依赖关系，给出重构建议"
```

## 和同类工具的对比

市场上类似的工具有 RepoPrompt、SourceGraph 等，但它们要么只支持 GitHub 仓库（需要在线操作），要么配置复杂。

Code2Prompt 的优势在于：

- **本地运行**，不依赖网络，你的代码不会上传到任何第三方服务器
- **安装极简**，一个 pip install 就完事了
- **模板系统灵活**，不限制你只能生成某种格式
- **价格透明**，生成之前就能看到 token 消耗和预估费用

缺点也有：对超大型项目（几千个文件）生成速度会变慢，因为需要读取和格式化每个文件。不过大部分项目用 `--filter` 缩小范围后完全够用。

## 总结

Code2Prompt 解决的是一个很具体的痛点：**让 AI 理解你的整个代码库，而不仅仅是当前文件**。

它不追求面面俱到，而是在「把代码上下文传给 LLM」这件事上做得足够好。安装简单、用法直观、输出质量稳定——对一个开源工具来说，这已经是很难得的品质了。

如果你平时经常用 AI 辅助编码，或者需要定期做代码审查和文档生成，值得给 Code2Prompt 五分钟试试。项目在 GitHub 上搜 `code2prompt` 就能找到，给作者点个 Star 也不亏。

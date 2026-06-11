---
title: "GeoMind：开源分析你的网页在AI搜索中的可见性"
date: 2026-06-11
draft: false
tags: ["开源", "GEO", "AI搜索", "CLI工具", "SEO", "凡森科技"]
---

Perplexity 月活过亿。ChatGPT Search 成为默认体验。Gemini 直接在搜索结果里给答案。Google 的 AI Overviews 覆盖了 84% 的查询。

用户正在习惯「不点链接」——AI 搜索直接把答案喂到眼前。这对内容网站意味着什么？如果你的页面没被 AI 搜索选中作为答案来源，你连被点击的机会都没有。

这件事正在催生一个新的品类：**GEO（Generative Engine Optimization，生成式引擎优化）**。和 SEO 优化的是「搜索引擎排名」不同，GEO 优化的是「AI 搜索是否选中你的内容作为答案来源」。

我写了一个开源工具叫 **GeoMind**，帮你快速知道自己的网页在 AI 搜索眼里长什么样。

![GeoMind CLI 输出示例](/images/geomind-arch.svg)

## 它解决什么问题

传统 SEO 工具给的是排名、流量预估、关键词难度。但 AI 搜索的评价体系完全不一样：

- 它能不能爬到你的内容？——有的前端渲染页面 AI 抓不到
- 它能不能理解你的内容？——结构化数据（JSON-LD）是 AI 的阅读指南
- 你的内容够不够「可引用」？——有来源、有日期、有事实的内容更容易被选中
- 你的站有没有权威性？——作者信息、联系方式、组织详情都会影响

这些维度传统 SEO 工具都不看，而 GeoMind 专门针对它们打分。

## 核心功能

```
geomind analyze <url>     → GEO 评分 + 分项分析
geomind suggest <url>     → 优化建议（按优先级排序）
geomind fetch <url>       → 获取 AI 抓取视角的页面内容
```

### GEO 评分

六维度评分体系，每项 0-100：

| 维度 | 权重 | 检查什么 |
|------|------|----------|
| 可爬取性 | 25% | AI 爬虫能否正常获取你的 HTML？JavaScript 渲染是否阻塞？ |
| 语义化 | 20% | 有没有 JSON-LD 结构化数据？Schema.org 类型是否正确？ |
| 内容质量 | 25% | 是否有事实、数据、对比、FAQ？段落是否充实？ |
| 可链接性 | 15% | 是否有稳定的锚点链接？是否引用权威外源？ |
| 权威性 | 10% | 作者/机构/联系方式是否明确？ |
| 性能 | 5% | 加载速度、图片 alt、HTML 大小是否合理？ |

### 实时输出

跑一下示例网站：

```
$ geomind analyze https://example.com

╭──────────────────────╮
│ GeoMind Report       │
│ https://example.com/ │
╰──────────────────────╯
Total Score: 37/100  FIX Weak

Dimension Scores:
  可爬取性    75/100  WATCH  ✅
  语义化      31/100  FIX    ❌
  内容质量     9/100  FIX    ❌
  可链接性    25/100  FIX    ❌
  权威性      10/100  FIX    ❌
  性能       100/100  OK     ✅
```

看到问题了吗？example.com 的性能拿满分，但语义化和内容质量只有个位数。这就是典型的技术网站通病——服务端响应快、页面干净，但 AI 搜索需要的结构化数据和深度内容几乎没有。

### 优化建议

```
  #  优先级  维度       建议                             
 ──────────────────────────────────────────────────── 
  1  High    内容质量    扩充页面：添加事实、示例、对比、FAQ  
  2  High    语义化      添加 JSON-LD Schema.org 标记    
  3  Medium  权威性      展示关于、联系方式、作者信息          
  4  Medium  可链接性    引用权威外源，创建带锚点的章节    
```

每一条建议都直接告诉你改什么、为什么改、怎么改。不是空泛的「提升内容质量」，而是具体的「添加 FAQ 结构」或「增加 JSON-LD 标记」。

## 架构设计

![GeoMind 架构图](/images/geomind-arch.svg)

整个工具围绕一个核心 pipeline：

1. **抓取层** — 用 requests + BeautifulSoup 获取页面，模拟 AI 爬虫视角
2. **分析层** — 六维度独立检查模块，各自打分
3. **报告层** — rich 终端输出 + 可分享 HTML 报告

每个检查模块独立、可测试，方便扩展新的 GEO 维度。

## 技术栈

- **Python 3.10+** — 零外部运行时依赖
- **requests + BeautifulSoup** — 网页抓取与解析
- **rich** — 终端彩色输出
- **Flask** — Web 演示界面（可选）

安装：

```bash
pip install -r requirements.txt
python geomind.py analyze https://yoursite.com
```

## 为什么做这个工具

GEO 正在从概念变成刚需。AI 搜索的流量分配方式和传统搜索完全不同：它是「选中即展示」，不是「排名靠前才展示」。这意味着内容的**可被引用性**比排名更重要。

但市面上没有简单好用的 GEO 诊断工具。大多数跨境 GEO 服务还是人工顾问模式，按项目收费。GeoMind 把这个能力做成一个开源 CLI，任何人 `pip install` 就能跑。

如果你是：
- 做内容网站/独立站的
- 做开发者工具的
- 做技术博客的
- 运营公司官网的

跑一下 `geomind analyze`，三分钟就知道你的页面在 AI 搜索眼里的真实处境。

## 后续计划

- 支持 Perplexity/ChatGPT Search 的引用来源分析
- 添加对比模式：你和竞品在 AI 搜索中的可见性差距
- HTML 报告模板优化，支持导出为分享链接
- 集成 GEO 监控：定时检查 + 趋势变化

## 链接

- GitHub：[coming soon]
- 项目官网：https://fansen.tech/geomind

---

如果你想在 AI 搜索中被找到，先知道自己在哪。

——Seb

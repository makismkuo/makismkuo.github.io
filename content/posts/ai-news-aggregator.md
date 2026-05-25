---
title: "自建 AI 新闻聚合器：从 14 个平台抓取 + 智能过滤 + 双语翻译"
date: 2026-05-25
draft: false
tags: ["AI", "开源", "RSS", "TypeScript", "部署", "前端"]
---

每天打开手机，各种 AI 新闻扑面而来。OpenAI 发了新模型、DeepSeek 又破纪录、Anthropic 推出新产品……信息量大到让人不知道怎么消化。

几个月前我试过不少方案。每天早上刷一遍 Twitter 上关注的那几个 AI 博主，打开几个新闻网站扫一眼标题，再点开几个微信群里转发的文章。这个过程大概花 20 分钟，但说实话，心里没什么底——总觉得自己漏掉了什么。

后来想想，与其被动地到处看，不如自己搭一个工具把信息聚拢过来。

## 为什么不做现成的

市面上做资讯聚合的产品不少。Google News、Feedly、Inoreader 这些老牌 RSS 阅读器都做得很好。但有两个问题让我一直没下决心用。

第一，**它们不够专注**。我说的是 AI 领域的信息，但通用阅读器会把财经、体育、政治全部混在一起。虽然有分类和关键词过滤功能，但要配出一个恰好只抓 AI 资讯的阅读器，需要花不少精力调。

第二，**语言问题**。我关注的 AI 信息源大部分是英文的——OpenAI、Anthropic、Hugging Face 的官方博客，Hacker News 上的讨论，Reddit 上的 r/MachineLearning 板块。每天快速扫标题的时候，英文标题看久了还是比中文慢一拍。如果能自动把英文标题翻译成中文，阅读效率会高很多。

就在想自己动手的时候，在 GitHub 上看到了 [ai-news-aggregator](https://github.com/SuYxh/ai-news-aggregator) 这个项目。它做的事情几乎和我想要的完全一样——从多个平台聚合 AI 资讯、自动过滤相关性、翻译英文标题为中文。而且它代码是开源的，TypeScript 写的，结构清晰。

决定把它部署起来，然后根据自己的需求做一些调整。

## 整体架构

![AI News Aggregator 架构图](/images/ai-news-arch.svg)

整个系统分成四层：

- **数据采集层**：从多个平台抓取资讯，每个平台对应一个 fetcher
- **数据处理层**：AI 相关性过滤、去重、标题翻译
- **数据输出层**：输出结构化的 JSON 文件
- **Web 展示层**：React SPA 前端，读取 JSON 文件做展示

每 2 小时跑一次完整的采集→处理→输出→部署流程，全部在 GitHub Actions 中完成。

## 数据源：14 个平台 + 70+ RSS + 52 个公众号

这个项目最打动我的地方是数据源的覆盖面。它不只有一个单一的抓取入口，而是针对每个平台写了一个独立的 fetcher。

### 聚合平台

像 TechURLs、TopHub、Buzzing 这类平台本身已经做了信息聚合的工作。TechURLs 每天汇总 Hacker News 和 Reddit 上最热门的技术文章，TopHub 覆盖了 50 多个平台的热门内容。从这些平台抓取，相当于一次拿到了多个源的数据。

```typescript
// 每个平台一个 fetcher，基类提供通用方法
class TechURLsFetcher extends BaseFetcher {
  siteId = 'techurls';
  siteName = 'TechURLs';

  async fetch(now: Date): Promise<RawItem[]> {
    // 从 HTML 中提取数据
    const $ = await this.fetchHtml('https://techurls.com/');
    // 解析页面结构，提取标题、链接、来源
    // ...
  }
}
```

每个 fetcher 的写法不一样，因为每个平台的前端渲染方式不同。有的用 SSR（服务端渲染），数据直接在 HTML 里；有的用 Next.js 的流式渲染，数据藏在 `__next_f.push` 里；有的 API 返回 JSON。

写 fetcher 的过程很像解谜题——打开开发者工具，看看数据在哪，怎么提取最稳。项目里对 Next.js 页面的数据提取做了一个通用的处理方案，从 `__NEXT_DATA__` script 标签里提取，如果找不到就降级到流式数据解析。这个双重降级策略在实际跑的时候很有用。

### RSS 订阅源

RSS 是传统但好用的方式。项目里通过一个 OPML 文件管理了 70 多个订阅源，涵盖顶级 AI 公司（OpenAI、Anthropic、Google DeepMind）、中国 AI 公司（阿里 Qwen、DeepSeek、腾讯混元）、AI 开发者工具（LangChain、LlamaIndex、Ollama）以及中文 AI 博主。

OPML 文件就是一堆 XML，结构大概是：

```xml
<outline text="AI 公司" title="AI 公司">
  <outline text="OpenAI Blog" type="rss" xmlUrl="https://openai.com/blog/rss.xml"/>
  <outline text="Anthropic Blog" type="rss" xmlUrl="https://anthropic.com/blog/rss.xml"/>
</outline>
```

解析 OPML 的时候有个细节：很多 RSS 源用的 RSSHub 地址不稳定，经常挂掉。项目里做了一个 URL 替换机制，把不稳定的 RSSHub 地址映射到官方源地址。这样即使 RSSHub 挂了，也能通过官方源继续抓取。

### 微信公众号

微信公众号是一个特殊的数据源。微信不对外开放 RSS 接口，所以需要通过第三方工具来采集。项目里通过 WeChat 公众号 RSS 服务来获取 52 个精选公众号的最新文章。覆盖范围包括机器之心、量子位、36氪、晚点LatePost 等。

这个模块我没有改太多，因为微信公众号的采集比较敏感，改动不好容易触发风控。按项目默认的配好，能稳定跑就行。

## 智能过滤：把噪音去掉

数据源多了以后，最大的问题不是信息太少，而是信息太多。一次抓取可能拿到几千条数据，但其中很多跟 AI 无关——比如 RSS 里混进来的科技财经新闻、某个平台的 bug 修复公告、完全不相关的社会新闻。

项目里的 AI 相关性过滤器做得比较实用：

```typescript
function isAiRelated(item: ArchiveItem): boolean {
  const text = `${title} ${source} ${siteName}`.toLowerCase();

  // AI 专用站点全部放行
  if (['aibase', 'aihot', 'aihubtoday'].includes(item.site_id)) {
    return true;
  }

  // 关键词匹配
  const aiKeywords = [
    'gpt', 'openai', 'anthropic', 'claude', 'gemini', 'deepseek',
    'llm', 'large language model', 'machine learning', 'deep learning',
    'neural network', 'transformer', 'rag', 'agent', 'copilot',
    'hugging face', 'langchain', 'llamaindex', 'diffusion',
  ];

  return aiKeywords.some(kw => text.includes(kw));
}
```

逻辑不复杂，但够用。AI 专用站点（如 AIBase、AI 今日热榜）的所有内容都放行，因为这些站点的内容本身就是筛选过的。其他源则通过关键词匹配来判断是否与 AI 相关。

除了 AI 相关性过滤，还有去重模块。同一个新闻可能在不同平台上出现（比如 OpenAI 发布新模型，TechURLs 有、TopHub 有、RSS 源也有），通过 title + URL 的 SHA1 哈希来去重。

## 翻译：解决语言焦虑

标题翻译是我最想用的功能。项目里用的是 Google 翻译 API（免费版），把英文标题翻译成中文。

翻译有一个缓存机制。已经翻译过的标题会存到 `title-zh-cache.json` 里，下次遇到相同的标题直接从缓存取，不重复调用 API。我看到的缓存文件已经有 17000 多条记录了，说明这个项目跑了有一段时间，翻译缓存帮了不少忙。

最终输出的数据格式是这样的：

```json
{
  "id": "sha1_hash",
  "site_id": "techurls",
  "site_name": "TechURLs",
  "source": "Reddit",
  "title": "GPT-5 即将发布 / GPT-5 Coming Soon",
  "url": "https://...",
  "published_at": "2026-05-25T08:00:00Z",
  "title_zh": "GPT-5 即将发布",
  "title_en": "GPT-5 Coming Soon"
}
```

双语标题的格式很方便，前端可以自由选择展示中文、英文还是双语。

## Web 前端

数据拿到之后，需要一个前端来展示。项目里内置了一个基于 React + TypeScript + Vite + Tailwind CSS 的单页应用。

它的功能覆盖了日常使用的各种需求：

- **多源筛选**：按平台、订阅源筛选，只看你关心的来源
- **关键词搜索**：在标题里搜索，快速定位特定话题
- **时间范围切换**：24 小时 / 7 天
- **收藏功能**：把感兴趣的文章收藏起来，稍后阅读
- **阅读历史**：自动记录你点开过的文章
- **暗色模式**：晚上看的时候不刺眼
- **数据导出**：把收藏的或筛选后的数据导出为 JSON

前端读取的是静态 JSON 文件，没有后端服务器。数据在 GitHub Actions 中生成后，直接作为静态文件部署到 GitHub Pages。整个应用就是一个纯静态站点，CDN 加速，加载速度很快。

## 部署过程

部署过程不算复杂，但有几个地方值得记一下。

### 本地运行

先拿下来跑一遍，确认所有配置都正常：

```bash
git clone https://github.com/SuYxh/ai-news-aggregator.git
cd ai-news-aggregator
pnpm install
pnpm fetch
```

`pnpm fetch` 会启动所有 fetcher，依次抓取各个平台的数据。第一次跑比较慢，因为要下载依赖、建立连接。跑完之后看 `data/` 目录，会生成最新一期的 JSON 文件。

如果只想测 OPML RSS，可以用：

```bash
pnpm fetch:opml ./feeds/follow.opml 5
```

最后的数字 5 表示只测试前 5 个 RSS 源，方便快速调试。

### 前端运行

切换到 `web/` 目录，安装依赖，启动 dev server：

```bash
cd web
pnpm install
pnpm dev
```

打开浏览器访问 `http://localhost:5173`，就能看到资讯流了。前端自动读取 `data/` 目录下的 JSON 文件，按时间倒序排列。

### 自动化部署

GitHub Actions 配置在 `.github/workflows/update-ai-news.yml` 里。核心逻辑是：

1. 每 2 小时触发一次定时任务
2. 运行 `pnpm fetch` 抓取最新数据
3. 构建前端 `cd web && pnpm build`
4. 部署到 `gh-pages` 分支

部署完之后，访问 `https://<用户名>.github.io/ai-news-aggregator/` 就能看到最新的资讯流了。

## 实际使用感受

跑起来到现在用了一段时间，说几点实际的感受。

**最大的好处是省时间。**以前每天早上刷各个渠道要花 20 分钟，现在打开一个页面，几分钟就能看完过去 24 小时最重要的 AI 动态。双语标题的体验确实比纯英文好，扫一眼中文标题就能判断要不要点进去看详情。

**覆盖度比想象的高。**我原来觉得自己关注的信息源已经挺多了，但用了这个聚合器之后发现还是漏了不少。比如 Papers With Code 上的热门论文、Hugging Face 上的新模型发布、一些中文 AI 博主的深度分析——之前没有系统性地关注过，现在都能在聚合器里看到。

**信息过载的问题并没有完全消失。**虽然有关键词过滤和去重，但每天仍然有几百条资讯。对于有时间逐条看的人来说这是好事，但如果只想知道"今天最大的新闻是哪条"，还是不够精炼。后来我调整了策略——每天早晚各看一次，重点关注 Top 10 的互动量高的文章，其他的当背景信息扫一眼即可。

**GitHub Actions 偶尔会失败。**大部分情况是某个数据源超时或返回了非预期的格式。项目里做了重试机制，但偶尔还是会卡住。我的做法是在 Actions 失败通知里看一眼，如果是单个源的问题，手动 rerun 就行，不影响其他源的数据。

## 一些改进方向

原项目已经做得很完善了，但根据自己的使用习惯，我想到几个可以改进的方向：

1. **用 LLM 做内容摘要**：目前只能看到标题，如果能用 AI 给每篇文章生成一句话摘要，扫读效率会更高。技术上不难，把标题和文章链接喂给 API 就行，但要注意控制成本。

2. **个性化权重**：有些源（比如 OpenAI 官方博客）的内容对我来说权重更高，但目前所有来源是一个平级的列表。如果能给数据源设置权重，高权重的源在列表里优先展示，会更符合个人习惯。

3. **关键词告警**：如果某条资讯包含特定的关键词（比如我关注的项目名），自动推送到 Telegram 上。这样即使没有打开聚合器，也不会错过重要信息。

这些改进打算后面慢慢加上去。

## 总结

从靠翻各个渠道被动接收信息，到用聚合器主动获取信息，这个转变带来的体验提升是实实在在的。搭建这个系统花了一两个小时，但每天节省的时间远超这个投入。

对于同样关注 AI 领域动态的朋友，我觉得这个项目值得一试。不管是用它作者部署好的在线版，还是自己 Fork 一份按需修改，成本都不高。代码是 MIT 许可的，随意使用。

如果你想试试，可以访问项目的 GitHub 仓库：`github.com/SuYxh/ai-news-aggregator`。

有什么问题欢迎交流。

——Seb

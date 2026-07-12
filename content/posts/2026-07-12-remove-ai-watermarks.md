---
title: "一键清除AI水印：remove-ai-watermarks 开源工具"
date: 2026-07-12
draft: false
tags: ["开源", "推荐", "GitHub", "AI", "CLI"]
---

## 项目简介

用 AI 生成图片很方便，但每个平台的"水印"让你很烦。Google Gemini 的闪光星星、Midjourney 的 C2PA 元标签、Stable Diffusion 在 EXIF 里的生成参数——它们占地方、影响观感，有时还导致下游平台误判成"AI 侵权内容"。

[remove-ai-watermarks](https://github.com/wiltodelta/remove-ai-watermarks)（⭐3947）是一个纯 Python CLI 工具，专门用来清除 AI 图片的各种水印。一行命令就能去掉可见的徽标和不可见的 SynthID、Metadata，而且又快又稳。项目遵循 Apache 2.0 协议，作者明确声明仅限于合法用途（你对自己生成的图片拥有自主权）。

## 核心功能

这个工具覆盖了三类水印：

- **可见水印**：自动识别并移除 Gemini/Nano Banana 闪光星标、豆包的"豆包AI生成"条幅、即梦的"★ 即梦AI"标志、三星 Galaxy AI 的文字标注等。检测在 CPU 上完成（基于模板匹配 NCC + numpy），填充支持三种后端：cv2（无依赖，最快）、MI-GAN（轻量）、big-LaMa（质量最高），`auto` 模式自动选最优。

- **不可见水印**：通过扩散模型重绘去除 SynthID、StableSignature、TreeRing 等嵌入水印。需要 GPU（CUDA / MPS），默认 ControlNet 管线保持文字和人脸结构清晰。通过 `--strength` 控制去除强度，`--humanize` 添加胶片颗粒消除"AI 感"。

- **元数据剥离**：清除 EXIF、C2PA、IPTC、XMP 中的"Made with AI"标签和生成参数。支持 PNG、JPEG、AVIF、HEIF、JPEG-XL，甚至视频容器（MP4/MOV/M4V）和音频文件（MP3/WAV/FLAC）的元数据。

额外功能：`identify` 子命令聚合所有信号（C2PA 签名、SynthID 代理、可见水印检测等）给出可信的"来源鉴定"结果；`erase` 命令支持用户指定矩形区域擦除任意内容，不限已知水印模板。

## 为什么值得关注

当前 AI 生成内容爆炸，水印问题非常现实。这个项目解决了几个痛点：

1. **一站式**：一个 CLI 搞定全部——不需要分别找工具去 PS 擦除、手动删 EXIF、再跑模型重绘。
2. **设计务实**：`auto` 模式自动选最优填充，`--sensitivity` 允许对边缘案例调整检测严格度，`--pipeline sdxl` 在无文字场景切换更轻量的管线。每个选项都有合理默认值，初学者也能用。
3. **安装友好**：支持 Homebrew、pipx、uv tool、conda（审核中）多种方式。Homebrew 安装的是纯 CLI 内核，不拖沉重的 ML 依赖；只有需要不可见水印去除时才装 `[gpu]` extra。
4. **非侵入**：默认保留文字和人脸细节（ControlNet），不是粗暴的全图重绘。`--adaptive-polish` 自动还原原始图像的细节层次，避免过度平滑。
5. **做得漂亮的开源提交**：CI 全绿、类型标注完善、测试覆盖到位、有 ComfyUI 自定义节点。第三方 Integrations 也在一一跟进。

## 简单示例

```bash
# 一行命令清除所有水印
remove-ai-watermarks all image.png -o clean.png

# 看看这张图是什么 AI 生成的
remove-ai-watermarks identify image.png --json

# 只去掉可见水印（CPU 立等可取）
remove-ai-watermarks visible image.png -o clean.png

# 批量处理整个目录
remove-ai-watermarks batch ./images/ --mode all

# 擦除任意区域（x,y,w,h）
remove-ai-watermarks erase image.png --region 1640,1930,400,100 -o clean.png
```

安装更是简单到极致：

```bash
# 推荐方式
pipx install git+https://github.com/wiltodelta/remove-ai-watermarks.git

# macOS/Linux 用户
brew install wiltodelta/tap/remove-ai-watermarks
```

## 总结

如果你用 AI 生成图片，或者需要批量处理素材的上游标记，`remove-ai-watermarks` 是目前最完整、最好用的开源方案。它不依赖闭源服务，全部本地运行，Apache 2.0 协议没有商用框框。一个 `pip install` 就能让自己的图片素材颜值回春——值得放进你的开发者工具箱。

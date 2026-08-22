---
name: read-image
description: 读取本地图片内容，调用 DeepSeek vision API（deepseek-v4-flash-vision-exp）识别并返回文字描述。当用户发送图片、拖入图片、或要求"看这张图/读这个图"时使用。
---

# 读图（read-image）

## 为什么需要
Claude Code 的 Read 工具对非 Anthropic 模型（deepseek-*）会返回 `[Unsupported Image]`，无法直接读图。本 skill 绕过该限制：用 Python 把图片 base64 后直接调用 DeepSeek 的 vision API，返回文字描述。

## 使用方式
用系统可用的 Python 运行脚本，第一个参数是图片绝对路径，第二个参数（可选）是自定义问题：

```bash
python read_image.py "D:\path\to\image.png"
python read_image.py "D:\path\to\image.png" "图中这段代码报了什么错？"
```

## 实现要点
- API key 从 `~/.claude/settings.json` 的 `ANTHROPIC_AUTH_TOKEN` 动态读取，不硬编码，可安全分享
- 图片内容会发送到 DeepSeek 服务器，请只用于可外发的图片（勿用于身份证、合同、机密等）
- 脚本不写任何临时文件，结果直接打印到终端，零磁盘占用

## 依赖
- Python 3（命令名 `python`；若不在 PATH 用 `python3` 或本机实际路径）
- 有效的 DeepSeek API key（在各自 `~/.claude/settings.json`）

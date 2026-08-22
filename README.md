# read-image

让 Claude Code 通过 DeepSeek vision API 读取本地图片的 skill。

## 背景

Claude Code 内置的 Read 工具对非 Anthropic 官方模型（如 `deepseek-*`）无法读图，会返回 `[Unsupported Image]`。本 skill 用 Python 把图片 base64 后直接调用 DeepSeek 的视觉模型（`deepseek-v4-flash-vision-exp`），返回文字描述，让 Claude Code 具备看图能力。

## 安装

1. 把 `read-image` 文件夹复制到 `~/.claude/skills/` 下
2. 重启 Claude Code
3. 在 `~/.claude/settings.json` 的 `env` 中配置 DeepSeek API key（`ANTHROPIC_AUTH_TOKEN`）

## 使用

给 Claude Code 发图片并说「看这张图」，或命令行直接运行：

```bash
python read_image.py "<图片路径>"
python read_image.py "<图片路径>" "自定义问题"
```

## 依赖

- Python 3
- DeepSeek API key

## 隐私与安全

- **图片会发送到 DeepSeek 服务器**：请勿用于身份证、合同、公司机密、私人照片等敏感图片。
- **API key 不随项目走**：脚本运行时从 `~/.claude/settings.json` 读取，仓库内不含密钥，可安全分享，各用各的账号计费。
- **只访问 DeepSeek**：网络请求仅指向 `api.deepseek.com`（HTTPS），不访问其他域名。

## License

[MIT](LICENSE)

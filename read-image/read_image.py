#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""读取本地图片，调用 DeepSeek vision API 识别内容。

用法:
    python read_image.py <图片路径> [自定义问题]

图片内容会发送到 DeepSeek 服务器，请只用于可外发的图片。
API key 从 ~/.claude/settings.json 动态读取，不硬编码。
脚本不写任何临时文件，结果直接打印到终端。
"""
import sys
import os
import json
import base64
import urllib.request
import urllib.error


def load_api_key():
    """从 ~/.claude/settings.json 读取 DeepSeek API key。"""
    home = os.path.expanduser("~")
    cfg_path = os.path.join(home, ".claude", "settings.json")
    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    return cfg["env"]["ANTHROPIC_AUTH_TOKEN"]


def main():
    if len(sys.argv) < 2:
        print("用法: python read_image.py <图片路径> [自定义问题]")
        sys.exit(1)

    img_path = sys.argv[1]
    question = (
        sys.argv[2]
        if len(sys.argv) > 2
        else "请详细描述这张图片里的所有内容，包括文字、数字、图表、界面元素、代码、硬件等。"
    )

    if not os.path.isfile(img_path):
        print("图片文件不存在:", img_path)
        sys.exit(1)

    # 大小检查：超过 30MB 拒绝，防止超大文件 base64 后内存爆炸
    max_size = 30 * 1024 * 1024  # 30MB
    file_size = os.path.getsize(img_path)
    if file_size > max_size:
        print("图片过大: %.1f MB（上限 30MB），请压缩后再试" % (file_size / 1024 / 1024))
        sys.exit(1)

    ext = os.path.splitext(img_path)[1].lower()
    mime_map = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }
    mime = mime_map.get(ext, "image/png")

    with open(img_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()

    payload = {
        "model": "deepseek-v4-flash-vision-exp",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": question},
                    {"type": "image_url", "image_url": {"url": "data:%s;base64,%s" % (mime, img_b64)}},
                ],
            }
        ],
    }

    key = load_api_key()
    req = urllib.request.Request(
        "https://api.deepseek.com/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + key},
    )
    try:
        resp = urllib.request.urlopen(req, timeout=120)
        result = json.loads(resp.read().decode("utf-8"))
        print(result["choices"][0]["message"]["content"])
    except urllib.error.HTTPError as e:
        print("HTTP 错误 %d: %s" % (e.code, e.read().decode("utf-8", errors="replace")))
        sys.exit(1)
    except Exception as e:
        print("调用失败: %s: %s" % (type(e).__name__, str(e)))
        sys.exit(1)


if __name__ == "__main__":
    # Windows 控制台默认 GBK，遇到特殊符号（箭头等）会报错，统一用 utf-8
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    main()

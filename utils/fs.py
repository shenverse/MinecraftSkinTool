# -*- coding: utf-8 -*-
"""文件与路径工具"""
import os
import sys
import time
import base64
import hashlib
import io

from PIL import Image

APP_NAME = "网易MC皮肤提取工具"
DESKTOP = os.path.join(os.path.expanduser("~"), "Desktop")
CONFIG_DIR = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "MC_Skin_Tool")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")
THUMB = 96


def resource_path(rel):
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(base, rel)


def dbg(*args):
    """写调试日志，路径固定在 APPDATA，不依赖 EXE 所在位置"""
    try:
        os.makedirs(CONFIG_DIR, exist_ok=True)
        with open(os.path.join(CONFIG_DIR, "api_log.txt"), "a", encoding="utf-8") as f:
            f.write(time.strftime("%H:%M:%S") + " " + " ".join(str(a) for a in args) + "\n")
    except Exception:
        pass


def file_digest(path):
    try:
        h = hashlib.md5()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return ""


def thumb_b64(path):
    """皮肤缩略图转 base64 data URL"""
    try:
        with Image.open(path) as im:
            im = im.convert("RGBA")
            im.thumbnail((THUMB, THUMB), Image.LANCZOS)
            buf = io.BytesIO()
            im.save(buf, format="PNG")
            return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode("ascii")
    except Exception:
        return ""


def load_config():
    cfg = {"download_dir": DESKTOP}
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = _json.load(f)
        if data.get("download_dir") and os.path.isdir(data["download_dir"]):
            cfg["download_dir"] = data["download_dir"]
    except Exception:
        pass
    return cfg


def save_config(cfg):
    try:
        os.makedirs(CONFIG_DIR, exist_ok=True)
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            _json.dump(cfg, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False


import json as _json

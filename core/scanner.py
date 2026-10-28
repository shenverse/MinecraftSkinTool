# -*- coding: utf-8 -*-
"""扫描引擎：网易版皮肤目录 + 全盘搜索，带去重与耗时保护"""
import os
import time

from core.detector import is_skin_png, MAX_TEXTURE_BYTES
from model.skin import Skin
from utils.fs import file_digest

NETEASE_APPDATA = os.path.join(os.environ.get("APPDATA", ""), "MinecraftPC_Netease_PB")
GAME_DIR = r"F:\mc"
MAX_ZIP_BYTES = 64 * 1024 * 1024      # 4D 皮肤包体积上限
MAX_WALK_DIRS = 4000                  # 网易数据目录遍历上限
DEFAULT_TIME_BUDGET = 60.0            # 已知目录扫描耗时上限（秒）

SKIP_PARTS = (
    "cache", "log", "temp", "tmp", "assets", "resource_packs",
    "shader", "behavior", "data", "download", "webcache",
    "deltas", "worlds", "backups", "update", "logs",
    "textures", "sounds", "lang", "structures",
    "clientcache", "packcache", "internalstorage",
    "bootstrapstorage", "exportworlds", "importworlds",
    "importresourcepacks", "minecraftpe", "minecraftworlds",
    "storge", "world_templates", "behavior_packs",
    "development_resource_packs", "development_behavior_packs",
)


def scan_dir(root, source, out, seen):
    """扫描单个目录：皮肤 PNG + 皮肤包 ZIP"""
    if not root or not os.path.isdir(root):
        return
    try:
        entries = sorted(os.listdir(root))
    except Exception:
        return
    for fn in entries:
        p = os.path.join(root, fn)
        if not os.path.isfile(p):
            continue
        ext = os.path.splitext(fn)[1].lower()
        try:
            size = os.path.getsize(p)
        except OSError:
            continue
        if ext == ".png" and is_skin_png(p):
            d = file_digest(p)
            if not d or d in seen:
                continue
            seen.add(d)
            out.append(Skin(p, fn, source, size, d))
        elif ext == ".zip" and 0 < size <= MAX_ZIP_BYTES:
            d = "z" + file_digest(p)
            if not d or d in seen:
                continue
            seen.add(d)
            out.append(Skin(p, fn, source + "（4D包）", size, d))


def scan_known(time_budget=DEFAULT_TIME_BUDGET):
    """网易版已知皮肤位置 + 数据目录遍历；超时自动截断，避免长时间卡死"""
    out, seen = [], set()
    t0 = time.time()

    def expired():
        return time.time() - t0 > time_budget

    scan_dir(os.path.join(NETEASE_APPDATA, "custom_skins"), "自定义皮肤", out, seen)
    scan_dir(os.path.join(NETEASE_APPDATA, "skin_packs"), "皮肤包", out, seen)
    scan_dir(os.path.join(NETEASE_APPDATA, "games", "com.netease", "skin_packs"), "商城/模组皮肤", out, seen)
    scan_dir(os.path.join(NETEASE_APPDATA, "games", "com.netease", "development_skin_packs"), "开发皮肤", out, seen)
    scan_dir(os.path.join(NETEASE_APPDATA, "games", "com.netease", "resource_packs"), "资源包", out, seen)

    if os.path.isdir(NETEASE_APPDATA):
        n_dirs = 0
        for dirpath, dirnames, filenames in os.walk(NETEASE_APPDATA):
            if expired():
                break
            n_dirs += 1
            if n_dirs > MAX_WALK_DIRS:
                break
            dirnames[:] = [d for d in dirnames
                           if not any(x in d.lower() for x in SKIP_PARTS)]
            low = dirpath.lower()
            if any(x in low for x in SKIP_PARTS):
                continue
            for fn in filenames:
                if not fn.lower().endswith(".png"):
                    continue
                p = os.path.join(dirpath, fn)
                try:
                    if os.path.getsize(p) > MAX_TEXTURE_BYTES:
                        continue
                except OSError:
                    continue
                if is_skin_png(p):
                    d = file_digest(p)
                    if not d or d in seen:
                        continue
                    seen.add(d)
                    rel = os.path.relpath(dirpath, NETEASE_APPDATA)
                    out.append(Skin(p, fn, rel, os.path.getsize(p), d))

    scan_dir(GAME_DIR, "游戏目录F:\\mc", out, seen)
    return out


def scan_full_disk(progress_cb=None, cancel_cb=None):
    """全盘搜索所有盘符中的皮肤贴图，支持进度与取消"""
    out, seen = [], set()
    drives = [l + ":\\" for l in "CDEFGH" if os.path.exists(l + ":\\")]
    n = 0
    for root in drives:
        try:
            for dirpath, dirnames, filenames in os.walk(root):
                if cancel_cb and cancel_cb():
                    return out, True
                n += 1
                if n % 500 == 0 and progress_cb:
                    progress_cb(dirpath)
                low = dirpath.lower()
                if any(x in low for x in ("\\windows", "\\program files", "\\programdata",
                                          "$recycle.bin", "\\appdata\\local\\temp", "node_modules")):
                    continue
                for fn in filenames:
                    p = os.path.join(dirpath, fn)
                    try:
                        if fn.lower().endswith(".png") and os.path.getsize(p) < 512 * 1024 and is_skin_png(p):
                            d = file_digest(p)
                            if not d or d in seen:
                                continue
                            seen.add(d)
                            out.append(Skin(p, fn, "全盘搜索", os.path.getsize(p), d))
                    except Exception:
                        pass
        except Exception:
            continue
    return out, False

# -*- coding: utf-8 -*-
"""皮肤贴图识别：只认 64x64 / 128x128 的 PNG 皮肤贴图"""
import os

from PIL import Image

SKIN_SIZES = {(64, 64), (128, 128)}
MAX_TEXTURE_BYTES = 256 * 1024


def is_skin_png(path):
    try:
        with Image.open(path) as im:
            return im.format == "PNG" and im.size in SKIN_SIZES
    except Exception:
        return False

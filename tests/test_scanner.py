# -*- coding: utf-8 -*-
"""扫描引擎单元测试"""
import os
import sys
import tempfile
import zipfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PIL import Image  # noqa: E402

from core.scanner import scan_dir, MAX_ZIP_BYTES  # noqa: E402


def _write_png(directory, name, size=(64, 64)):
    im = Image.new("RGBA", size, (200, 100, 50, 255))
    p = os.path.join(directory, name)
    im.save(p, format="PNG")
    return p


def test_scan_dir_finds_png_and_zip():
    with tempfile.TemporaryDirectory() as d:
        _write_png(d, "a.png")
        zpath = os.path.join(d, "pack.zip")
        with zipfile.ZipFile(zpath, "w") as z:
            z.writestr("x.txt", "1")
        out, seen = [], set()
        scan_dir(d, "测试", out, seen)
        names = {s.name for s in out}
        assert "a.png" in names
        assert "pack.zip" in names


def test_scan_dir_dedup():
    with tempfile.TemporaryDirectory() as d:
        _write_png(d, "a.png")
        out, seen = [], set()
        scan_dir(d, "测试", out, seen)
        scan_dir(d, "测试", out, seen)
        assert len(out) == 1


def test_scan_dir_skips_big_zip():
    with tempfile.TemporaryDirectory() as d:
        zpath = os.path.join(d, "big.zip")
        with open(zpath, "wb") as f:
            f.write(b"0" * (MAX_ZIP_BYTES + 1))
        out, seen = [], set()
        scan_dir(d, "测试", out, seen)
        assert not any(s.name.endswith(".zip") for s in out)

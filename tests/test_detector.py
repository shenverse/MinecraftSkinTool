# -*- coding: utf-8 -*-
"""皮肤识别单元测试"""
import io
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PIL import Image  # noqa: E402

from core.detector import is_skin_png, SKIN_SIZES  # noqa: E402


def _make_png(size, name, directory):
    im = Image.new("RGBA", size, (80, 160, 60, 255))
    p = os.path.join(directory, name)
    im.save(p, format="PNG")
    return p


def test_accepts_skin_sizes():
    with tempfile.TemporaryDirectory() as d:
        for size in SKIN_SIZES:
            p = _make_png(size, "skin_%dx%d.png" % size, d)
            assert is_skin_png(p) is True


def test_rejects_wrong_sizes():
    with tempfile.TemporaryDirectory() as d:
        p = _make_png((32, 32), "small.png", d)
        assert is_skin_png(p) is False


def test_rejects_non_png():
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "fake.png")
        with open(p, "wb") as f:
            f.write(b"not an image")
        assert is_skin_png(p) is False

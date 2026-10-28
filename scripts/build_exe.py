# -*- coding: utf-8 -*-
"""PyInstaller 打包脚本：生成单文件 EXE
用法: python scripts/build_exe.py
产物: dist/网易MC皮肤提取工具.exe
"""
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_NAME = "网易MC皮肤提取工具"


def main():
    import PyInstaller.__main__ as pyi

    work = os.path.join(ROOT, "build")
    out = os.path.join(ROOT, "dist")
    if os.path.isdir(out):
        shutil.rmtree(out, ignore_errors=True)

    args = [
        os.path.join(ROOT, "main.py"),
        "--name", APP_NAME,
        "--onefile",
        "--windowed",
        "--noconfirm",
        "--clean",
        "--workpath", work,
        "--distpath", out,
        "--add-data", os.path.join(ROOT, "app", "ui.html") + os.pathsep + "app",
    ]
    pyi.run(args)
    exe = os.path.join(out, APP_NAME + ".exe")
    print("EXE:", exe, os.path.getsize(exe) // 1024, "KB")


if __name__ == "__main__":
    main()

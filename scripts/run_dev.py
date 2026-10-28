# -*- coding: utf-8 -*-
"""开发模式直接运行（不打包），用于调试"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from main import main  # noqa: E402

if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""程序入口"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.bridge import Api  # noqa: E402
from utils.fs import resource_path, APP_NAME  # noqa: E402


def main():
    import webview
    api = Api()
    window = webview.create_window(
        APP_NAME,
        url=resource_path(os.path.join("app", "ui.html")),
        js_api=api,
        width=1120, height=740,
        min_size=(860, 600),
        background_color="#F2F4F7",
    )
    api._window = window
    webview.start()


if __name__ == "__main__":
    main()

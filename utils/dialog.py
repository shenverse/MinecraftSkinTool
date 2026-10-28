# -*- coding: utf-8 -*-
"""原生对话框：tkinter 封装（pywebview 自带对话框在子线程静默失败，改用此方案）"""


def pick_folder():
    import tkinter as tk
    from tkinter import filedialog
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    try:
        return filedialog.askdirectory(title="选择皮肤下载保存位置")
    finally:
        root.destroy()

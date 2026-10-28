# -*- coding: utf-8 -*-
"""皮肤数据模型"""


class Skin:
    """一个候选皮肤文件：路径、名称、来源、体积、去重指纹"""

    def __init__(self, path, name, source, size, digest):
        self.path = path
        self.name = name
        self.source = source
        self.size = size
        self.digest = digest
        self._thumb = None

    def to_dict(self):
        from utils.fs import thumb_b64
        if self._thumb is None:
            self._thumb = thumb_b64(self.path)
        return {
            "path": self.path,
            "name": self.name,
            "source": self.source,
            "size": self.size,
            "thumb": self._thumb,
            "isZip": self.name.lower().endswith(".zip"),
        }

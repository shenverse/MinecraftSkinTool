# -*- coding: utf-8 -*-
"""pywebview 桥接层：后端能力暴露给前端 JS"""
import os
import shutil
import threading
import time
import traceback

from core.scanner import scan_known, scan_full_disk
from utils.fs import dbg, load_config, save_config, DESKTOP, APP_NAME
from utils.dialog import pick_folder


class Api:
    def __init__(self, window=None):
        self._window = window
        self.cfg = load_config()
        self._skins = []
        self._lock = threading.Lock()
        self._cancel_full = False

    def app_info(self):
        return {"name": APP_NAME, "download_dir": self.cfg["download_dir"]}

    def scan(self):
        try:
            t0 = time.time()
            with self._lock:
                self._skins = scan_known()
                items = [s.to_dict() for s in self._skins]
            dbg("scan ok", len(items), "in %.1fs" % (time.time() - t0))
            return {"ok": True, "count": len(items), "items": items}
        except Exception as e:
            dbg("scan FAIL", repr(e), traceback.format_exc())
            return {"ok": False, "error": str(e)}

    def cancel_full_scan(self):
        self._cancel_full = True
        return {"ok": True}

    def full_scan(self):
        self._cancel_full = False

        def prog(p):
            try:
                self._window.evaluate_js(
                    "window.__fullScanProgress && window.__fullScanProgress(%s)"
                    % _json_dumps(p, ensure_ascii=False)
                )
            except Exception:
                pass

        found, cancelled = scan_full_disk(progress_cb=prog, cancel_cb=lambda: self._cancel_full)
        with self._lock:
            known = {s.digest for s in self._skins}
            added = 0
            for s in found:
                if s.digest and s.digest not in known:
                    self._skins.append(s)
                    known.add(s.digest)
                    added += 1
            items = [s.to_dict() for s in self._skins]
        return {"ok": True, "cancelled": cancelled, "added": added, "count": len(items), "items": items}

    def download(self, path, name):
        try:
            base, ext = os.path.splitext(name)
            dl = self.cfg.get("download_dir") or DESKTOP
            target = os.path.join(dl, name)
            n = 1
            while os.path.exists(target):
                target = os.path.join(dl, f"{base}({n}){ext}")
                n += 1
            shutil.copy2(path, target)
            return {"ok": True, "target": target}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def get_settings(self):
        return {"download_dir": self.cfg["download_dir"]}

    def choose_dir(self):
        try:
            d = pick_folder()
            if not d:
                return {"ok": False, "cancel": True}
            if not os.path.isdir(d):
                return {"ok": False, "error": "所选目录不存在"}
            self.cfg["download_dir"] = d
            save_config(self.cfg)
            return {"ok": True, "download_dir": d}
        except Exception as e:
            return {"ok": False, "error": str(e)}


def _json_dumps(obj, **kw):
    import json
    return json.dumps(obj, **kw)

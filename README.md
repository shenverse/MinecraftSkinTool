# 网易 MC 皮肤提取工具

把网易版《我的世界》下载过的皮肤一键提取出来，导出成 Java 版可以直接用的皮肤文件。

纯本地扫描，不联网、无遥测、不含任何第三方 API。

## 功能

- 自动定位网易版皮肤目录（自定义皮肤 / 皮肤包 / 商城模组皮肤 / 开发皮肤）
- 数据目录深度遍历 + 去重，不漏不重
- 全盘搜索兜底，可随时停止
- 缩略图预览，按来源与体积标注
- 一键导出到自定义目录（默认桌面），重名自动加序号
- 4D 皮肤包（zip）一并列出，保留原文件导出

## 运行环境

- Windows 10 / 11
- Python 3.9+
- 依赖：`pywebview`、`Pillow`

## 快速开始

```bash
pip install -r requirements.txt
python main.py
```

## 打包 EXE

```bash
python scripts/build_exe.py
```

产物在 `dist/网易MC皮肤提取工具.exe`，单文件，无需安装。

## 测试

```bash
python -m pytest tests -v
```

## 目录结构

```
MinecraftSkinTool/
├── main.py                 # 程序入口
├── core/                   # 扫描引擎
│   ├── scanner.py          #   已知目录 / 全盘扫描，去重与耗时保护
│   └── detector.py         #   皮肤贴图识别（64/128 PNG）
├── model/                  # 数据模型
│   └── skin.py             #   Skin 实体
├── app/                    # 应用层
│   ├── bridge.py           #   pywebview 桥接 API
│   └── ui.html             #   前端界面（图标内嵌，单文件自包含）
├── utils/                  # 工具集
│   ├── fs.py               #   文件摘要 / 缩略图 / 配置
│   └── dialog.py           #   原生文件夹选择
├── scripts/                # 构建脚本
│   ├── build_exe.py        #   PyInstaller 打包
│   └── run_dev.py          #   开发模式运行
├── tests/                  # 单元测试
└── docs/                   # 文档
```

## 原理

网易版皮肤贴图为 64×64 / 128×128 PNG，存放在 `%APPDATA%\MinecraftPC_Netease_PB` 与 `%APPDATA%\MinecraftPC_Netease_PB\games\com.netease` 下。工具按目录特征扫描、MD5 去重，命中即列入候选。扫描带目录数与耗时双重上限，避免异常数据目录拖死程序。

## License

[MIT](LICENSE)

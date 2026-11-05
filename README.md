# MIB STD2 Toolbox 汉化版（简体中文 / zh-CN）

> **实验性汉化，尚未在真机上测试。** 这是一个把绿菜单界面译成简体中文的非官方衍生版本，功能与原版完全一致，只改了界面文字。
>
> **公开项目，欢迎任何人提交改动与修正** —— 尤其是真机测试报告（能显示中文 / 显示方框 / 乱码），这对本项目价值最大。

[![status](https://img.shields.io/badge/status-experimental-orange)](#%E5%BD%93%E5%89%8D%E7%8A%B6%E6%80%81)
[![tested](https://img.shields.io/badge/on--car%20test-not%20yet-red)](#%E5%BD%93%E5%89%8D%E7%8A%B6%E6%80%81)
[![platform](https://img.shields.io/badge/platform-MIB2%20STD2%20PQ%2FZR-blue)](#%E9%80%82%E7%94%A8%E8%8C%83%E5%9B%B4)
[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## 这是什么

把 [olli991/mib-std2-pq-zr-toolbox](https://github.com/olli991/mib-std2-pq-zr-toolbox) **v1.5.1** 的绿菜单工程界面（GEM）汉化成简体中文的衍生版本。

- 目标机型：**MIB2 Standard（STD2）PQ / ZR**，TechniSat / Preh 机器，例如国行 `MST2_CN_VW_PQ_P0480T`、软件串 `H29.319.93_STD2NavPQ_CHN` 这类 682F 主机
- 改动内容：**只改 `cpu/onlineservices/1/default/tsd/etc/persistence/esd/*.esd` 里的界面文字**
- 未改动：`metainfo2.txt`（逐字节等于上游，`MetafileChecksum = c7ecf8e46fb5915962f2d831a9460974a3f5f8a0` 已验证自洽）、所有 `.sh` 脚本、所有 jar、所有 SWDL 结构
- `cpu/` 目录结构与上游一致，**本仓库根目录就是 SD 卡根目录**，下载解压后可直接拷到 FAT32 卡上使用

## 下载

| 方式 | 链接 | 说明 |
|---|---|---|
| 打好的 zip（推荐） | [Releases → v1.5.1-zh.1](https://github.com/ffranx/mib-std2-toolbox-zh-cn/releases/tag/v1.5.1-zh.1) | `MIB2-Toolbox-zh-CN-v1.5.1.zip`，解压即卡根 |
| 仓库直接下载 | 本页 `Code → Download ZIP` | 仓库根目录**就是** SD 卡根目录，解压后直接用 |

打好的 zip 校验：

```
SHA256  8735960bf3f1bedcc9f7f472a1ecfd61da893369bae1a84618b7bc4c8b31cd96
文件大小 591865 字节（578 KB）
```

## 当前状态

| 项 | 状态 |
|---|---|
| 界面文字汉化 | ✅ 已完成 122 条（主菜单、自定义、导出、工具、网络、皮肤、导航、按键、绿菜单、更新与卸载等） |
| 编码/结构校验 | ✅ 离线通过（无 BOM、CRLF 一致、无控制字符、引号闭合、宽度 ≤34 格） |
| **真机验证** | ❌ **还没做过** —— 本项目由协作者在电脑上生成，没有实车/实机测试 |
| 中文字形是否可显示 | ❓ 未知。`GEM.jar` 内不含字体文件，能否显示中文取决于车机固件里的 J9 字库 |

**已知的最大未知项**：GEM 是 Java 界面，文字由车机 JVM 的字型渲染。部分固件可能没有中文字形，届时中文会显示为**方框或空白**。因此包里放了一张探测屏 `ZhProbe`（见下）。

## 上游来源与授权

| 项 | 内容 |
|---|---|
| 上游项目 | [olli991/mib-std2-pq-zr-toolbox](https://github.com/olli991/mib-std2-pq-zr-toolbox) |
| 上游版本 | v1.5.1（`MIBSTD2_Toolbox-v1.5.1.zip`，SHA256 `cf74a774f4ba1842abb1b5fb3db71a2deba6d6691844de0ab1d32178750ee9a6`） |
| 上游作者 | Olli、lprot、YOX 等（见 `docs/upstream-README.en.md`） |
| 上游许可 | MIT（`LICENSE`，Copyright (c) 2021 olli991） |
| 本项目性质 | 非官方汉化衍生版，**与原项目/作者无关联，未获官方背书** |
| 本项目许可 | 同样 MIT，保留原版权声明 |

上游 README 原文保留在 [`docs/upstream-README.en.md`](docs/upstream-README.en.md)，汉化技术细节见 [`docs/汉化说明.md`](docs/汉化说明.md)。

## 适用 / 不适用

| 平台 | 是否适用 |
|---|---|
| MIB2 Standard PQ/ZR（TechniSat/Preh） | ✅ 适用 |
| MIB2 Standard Delphi | ❌ 不适用（上游同样不支持） |
| MIB2 High / 2.5 High（Discover Pro，`MHI2_*`） | ❌ 不适用，请用 [jilleb/mib2-toolbox](https://github.com/jilleb/mib2-toolbox) 或 [M.I.B.](https://github.com/Mr-MIBonk/M.I.B._More-Incredible-Bash) |
| MIB1 | ❌ 不适用 |

## 安装（与上游完全相同，走 SWDL）

1. FAT32 格式化空卡（≥1 GB，MBR），把**本仓库全部内容**解压到卡根 —— 解压后卡根必须直接看到 `metainfo2.txt`，不要再套一层目录。
2. 着车或接充电器，卡插 **SD1**，机内不要留第二张卡。
3. 长按 **MENU** 约 10 秒 → `Service Mode` → `Software Update` → 选卡 → `MIBStd2_Online_Approval` → 安装。
4. 装完进 **GEM**（绿菜单），会多出 `MIB工具箱` 一项。

### 装完先验字形

绿菜单里进 **`MIB工具箱 → ZhProbe`**，这一屏会同时显示 ASCII、中文、边界汉字：

| 你看到 | 说明 | 建议 |
|---|---|---|
| 中文正常 | 字库支持中文 | 直接用这版 |
| 中文变成 **方框 / 空白** | GEM 无中文字形 | 用回官方英文版，本汉化包对你无意义 |
| 中文变 **乱码**（能看出是字但是错的） | 编码不匹配 | 说明是 GBK/UTF-8 问题，请提 issue 报固件版本 |

请把结果提到 [Issues](../../issues)，写明：`Train` 串、主机件号、GEM 版本（绿菜单左上角）、`ZhProbe` 截图。这些信息能直接决定汉化包是否需要换编码重新生成。

## 与上游的差异清单

| 文件 | 变化 |
|---|---|
| `cpu/.../esd/mibstd2-*.esd` | 界面文字改为简体中文（122 条） |
| `cpu/.../esd/zzprobe-utf8.esd` | **新增**：中文字形探测屏 |
| `cpu/.../esd/zzprobe-gbk.esd` | **新增**：同上，GBK 编码版本（用于判断乱码是否由编码引起） |
| `metainfo2.txt` | 无改动（`SkipFileCopyChecksum = "true"`，载荷文件本来就不校验） |
| 其它（脚本/jar/结构） | 无改动 |

> 注意：`zzprobe-gbk.esd` 是刻意为非 UTF-8 的文件，用编辑器打开会显示乱码，属正常现象。

## 自己重建 / 参与汉化

```bash
# 需要 Python 3.8+
python zh-tools/localize_esd.py --src <上游v1.5.1解压目录> --out out \
        --map zh-tools/zh_map.json --encoding utf-8 --sanitize ascii
python zh-tools/check_esd.py --dir out/cpu/onlineservices/1/default/tsd/etc/persistence/esd --width 34
python zh-tools/pack.py   # 生成可直接解压到 SD 卡的 zip
```

- 文案都在 [`zh-tools/zh_map.json`](zh-tools/zh_map.json)：`labels` 是屏内文字，`screens` 是菜单项名字
- 未翻译条目清单见 [`docs/localize-report.txt`](docs/localize-report.txt)（剩余约 1000 条，多为车辆适配通道名）
- 排版硬约束（违反会导致整屏不显示）：UTF-8 **无 BOM**、CRLF、label 内不能出现 ASCII 双引号、宽度 ≤34 格（汉字算 2）、标点优先半角

## 贡献

欢迎 PR。优先需要的贡献类型，按价值排序：

1. **真机测试报告**（截图 + Train 串 + GEM 版本）—— 直接决定项目是否可用
2. **译文修正 / 补全**（改 `zh-tools/zh_map.json` 即可，附上屏名）
3. **宽度/排版修正**（跑 `check_esd.py` 把超宽条目压下来）
4. **GBK 版验证**（部分固件只吃 GBK，需要有人实测）
5. 新的上游版本跟进（上游发新版后重新套用映射表）

提交前请跑一遍 `check_esd.py`，确保"问题"段没有新增项。细节见 [`CONTRIBUTING.md`](CONTRIBUTING.md)。

## 风险

刷写类操作本身有风险：断电变砖、装机失败、菜单错乱。本汉化只改界面文本，不动固件、不动校验、不动脚本，但**仍建议先做 eMMC 备份**（工具箱内 `导出 → eMMC content`，需 exFAT 卡 + 约 7.3 GB 空间）。

## English (short)

An **experimental, untested** Simplified-Chinese localization of [olli991/mib-std2-pq-zr-toolbox](https://github.com/olli991/mib-std2-pq-zr-toolbox) v1.5.1 for MIB2 **Standard (STD2) PQ/ZR** units. Only GEM screen texts inside `*.esd` were translated; `metainfo2.txt`, scripts and jars are untouched (MIT, upstream attribution kept). Not affiliated with the upstream authors. Chinese glyph rendering is **unverified** — boot the `ZhProbe` screen first. PRs (especially on-car test reports) are welcome.

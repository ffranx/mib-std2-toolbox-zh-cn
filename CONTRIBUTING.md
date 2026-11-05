# 参与贡献

这个项目的价值全在"真机反馈"上，欢迎任何形式的修正。

## 最有用的三种提交

### 1. 真机测试报告（Issue）

请附：

```
主机件号      : 例如 5C0035682F
软件版本串    : 例如 H29.319.93_STD2NavPQ_CHN
Train        : Service Mode → 软件版本页
GEM 版本      : 绿菜单左上角，例如 4.11
ZhProbe 现象  : 中文正常 / 方框空白 / 乱码
截图          : ZhProbe 那一屏
```

如果是**方框/空白**，说明该固件的 J9 字库没有中文字形，这版汉化对你无效 —— 也请报一下，方便在 README 里维护"已知不支持的固件"清单。

### 2. 译文修正（PR）

1. 打开 `zh-tools/zh_map.json`
2. `labels` 里改中文（键必须与英文原文逐字一致，含标点与大小写）
3. 跑一遍校验：

```bash
python zh-tools/localize_esd.py --src <上游解压目录> --out out --map zh-tools/zh_map.json --encoding utf-8 --sanitize ascii
python zh-tools/check_esd.py --dir out/cpu/onlineservices/1/default/tsd/etc/persistence/esd --width 34
```

4. 把 `out/` 里被改动的 `.esd` 一并提交（本仓库根目录就是成品，保持同步）

### 3. 排版修正

`check_esd.py` 报出来的问题按这个优先级修：

| 问题 | 必须修 | 说明 |
|---|---|---|
| BOM / 行尾不统一 / label 内 ASCII 引号 / 控制字符 / screen 名含空格 | ✅ 必须 | 会导致整屏不显示 |
| 译文宽度 > 34 格 | 建议 | 会让右侧勾选框被挤掉 |
| 全角标点 / 全角数字 | 建议 | 字库可能缺字形，`--sanitize ascii` 可自动压掉 |

> 上游自己就有 77 条 label 超过 34 格，说明 GEM 对超宽是截断而不是报错，所以宽度属于"看不清"级别，不是"用不了"级别。

## 排版硬规范

| 项 | 正确 | 错误 |
|---|---|---|
| 编码 | UTF-8 无 BOM（或按需 GBK） | 带 BOM 的 UTF-8 |
| 行尾 | CRLF | 混用 CRLF/LF |
| 引号 | 不用；必须时用「」 | ASCII `"`（会截断字符串） |
| 宽度 | ≤34 格（汉字 2 格） | 长句堆一行 |
| 标点 | 半角 `, . : ; ( )` | 全角 `，。：；（）` |
| 省略/破折 | `..` / `--` | `……` `——` |
| 单位数字 | `16G 约1.5h` | `１６Ｇ 约１.５小时` |
| screen 名 | 无空格（如 `MIB工具箱`） | 含空格（会切坏菜单树） |

## 不要做的事

- 不要修改 `value` / `poll` / `script` 路径 / `choice` 寄存器地址 —— 这些是功能本体
- 不要动 `metainfo2.txt`（改了校验值就对不上，SWDL 直接报 `invalid metainfo checksum`）
- 不要把 `.esd` 当二进制"顺手格式化"（编辑器自动改行尾同样会破坏内容）

## 提交信息建议

```
zh: 修正 Navigation 屏 "双导航" 译文过长
zh: 补全 Tools → Privacy 一节 12 条
test: 682F / MST2_CN_VW_PQ_P0480T / GEM 4.11 —— 中文正常显示
```

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
localize_esd.py - MIB STD2 Toolbox (GEM 绿菜单) 汉化工具

原理：
  GEM 的每一个界面都是 cpu/onlineservices/1/default/tsd/etc/persistence/esd/*.esd
  纯文本文件。可见文案只有两种来源：
    1) 菜单项名字 --->  `screen <本屏名字> <父屏名字>` 里的 <本屏名字>
    2) 屏内文字   --->  `label "..."` 里的字符串（keyValue / script / choice 都是这个字段）

用法：
  python localize_esd.py --src ..\\src --out ..\\out --map ..\\zh_map.json --encoding utf-8
  python localize_esd.py --src ..\\src --out ..\\out-screens --map ..\\zh_map.json --screens

注意：
  * .esd 原文件是 CRLF + 纯 ASCII，本脚本默认按 ASCII 读、按 --encoding 写，行尾保持 CRLF。
  * --screens 会一并替换菜单项名字，属于实验性功能（部分固件的解析器可能不吃非 ASCII 的 screen 名）。
  * 用 --encoding gbk 可以试 GBK；多数 QNX/J9 环境把字节当 Latin-1 处理，UTF-8 更容易变乱码，
    所以务必先用 zh-probe 屏在车上实测哪条能正常显示。
"""
import argparse
import json
import os
import re
import sys

LABEL_RE = re.compile(r'(label\s+)"([^"]*)"')
SCREEN_RE = re.compile(r'(?m)^(screen\s+)(\S+)(\s+)(\S+)')


# 全角 -> 半角（字形最安全：半角标点一定在字库里）
PUNCT_MAP = {
    '，': ',', '。': '.', '、': ',', '；': ';', '：': ':',
    '！': '!', '？': '?', '（': '(', '）': ')', '【': '[', '】': ']',
    '《': '<', '》': '>', '“': '"', '”': '"', '‘': "'", '’': "'",
    '…': '..', '—': '--', '～': '~', '　': ' ',
    '０': '0', '１': '1', '２': '2', '３': '3', '４': '4',
    '５': '5', '６': '6', '７': '7', '８': '8', '９': '9',
    'Ａ': 'A', 'Ｂ': 'B', 'Ｃ': 'C', 'Ｄ': 'D', 'Ｅ': 'E',
}


def sanitize(s, mode):
    """把译文压成"字形最保险"的形态，避免全角标点/全角数字在车机字库里缺字形。"""
    if mode != 'ascii':
        return s
    for k, v in PUNCT_MAP.items():
        s = s.replace(k, v)
    # 去掉首尾空白与重复空格
    s = ' '.join(s.split())
    return s


def load_map(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    labels = data.get('labels', {})
    screens = data.get('screens', {})
    return labels, screens


def process_text(text, labels, screens, use_screens, stats, sanitize_mode='none'):
    def repl_label(m):
        src = m.group(2)
        if src in labels:
            dst = sanitize(labels[src], sanitize_mode)
            stats['labels_changed'] += 1
            stats['changed_pairs'].append((src, dst))
            return f'{m.group(1)}"{dst}"'
        if src.strip():
            stats['labels_missing'].add(src)
        return m.group(0)

    text = LABEL_RE.sub(repl_label, text)

    if use_screens:
        def repl_screen(m):
            name, parent = m.group(2), m.group(4)
            new_name = screens.get(name, name)
            new_parent = screens.get(parent, parent)
            if new_name != name:
                stats['screens_changed'] += 1
            return f'{m.group(1)}{new_name}{m.group(3)}{new_parent}'

        text = SCREEN_RE.sub(repl_screen, text)

    return text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', required=True, help='v1.5.1 解压出来的根目录')
    ap.add_argument('--out', required=True, help='输出目录（会整份复制 src 再改 esd）')
    ap.add_argument('--map', required=True, help='zh_map.json')
    ap.add_argument('--encoding', default='utf-8', choices=['utf-8', 'gbk', 'ascii'])
    ap.add_argument('--screens', action='store_true', help='同时汉化菜单项名字（实验性）')
    ap.add_argument('--sanitize', default='none', choices=['none', 'ascii'], help='ascii: 全角标点/数字压成半角，字形最保险')
    ap.add_argument('--report', default=None, help='报告输出路径，默认 <out>/localize-report.txt')
    args = ap.parse_args()

    labels, screens = load_map(args.map)
    esd_rel = os.path.join('cpu', 'onlineservices', '1', 'default', 'tsd', 'etc', 'persistence', 'esd')
    src_esd = os.path.join(args.src, esd_rel)
    if not os.path.isdir(src_esd):
        sys.exit(f'找不到 esd 目录: {src_esd}')

    total = {'labels_changed': 0, 'screens_changed': 0, 'labels_missing': set(), 'changed_pairs': []}
    per_file = {}

    for root, _dirs, files in os.walk(args.src):
        for name in files:
            s = os.path.join(root, name)
            rel = os.path.relpath(s, args.src)
            d = os.path.join(args.out, rel)
            os.makedirs(os.path.dirname(d), exist_ok=True)

            if name.lower().endswith('.esd'):
                with open(s, 'rb') as f:
                    raw = f.read()
                try:
                    text = raw.decode('ascii')
                except UnicodeDecodeError:
                    text = raw.decode('latin-1')
                stats = {'labels_changed': 0, 'screens_changed': 0,
                         'labels_missing': set(), 'changed_pairs': []}
                new_text = process_text(text, labels, screens, args.screens, stats, args.sanitize)
                total['labels_changed'] += stats['labels_changed']
                total['screens_changed'] += stats['screens_changed']
                total['labels_missing'] |= stats['labels_missing']
                total['changed_pairs'] += stats['changed_pairs']
                per_file[rel] = stats
                with open(d, 'wb') as f:
                    f.write(new_text.encode(args.encoding, errors='replace'))
            else:
                with open(s, 'rb') as f:
                    data = f.read()
                with open(d, 'wb') as f:
                    f.write(data)

    report = []
    report.append(f'src          : {os.path.abspath(args.src)}')
    report.append(f'out          : {os.path.abspath(args.out)}')
    report.append(f'encoding     : {args.encoding}')
    report.append(f'screens mode : {args.screens}')
    report.append(f'sanitize     : {args.sanitize}')
    report.append(f'label 替换    : {total["labels_changed"]} 处')
    report.append(f'screen 替换   : {total["screens_changed"]} 处')
    report.append(f'未翻译 label  : {len(total["labels_missing"])} 条（去重）')
    report.append('')
    report.append('--- 按文件 ---')
    for rel in sorted(per_file):
        st = per_file[rel]
        if st['labels_changed'] or st['screens_changed']:
            report.append(f'{os.path.basename(rel):34s} labels={st["labels_changed"]:3d} screens={st["screens_changed"]:3d}')
    report.append('')
    report.append('--- 未翻译的 label（照着往 zh_map.json 里加） ---')
    for s in sorted(total['labels_missing']):
        report.append('  ' + s)

    out_report = args.report or os.path.join(args.out, 'localize-report.txt')
    os.makedirs(os.path.dirname(out_report), exist_ok=True)
    with open(out_report, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    print('\n'.join(report[:8]))
    print(f'\n报告已写入: {out_report}')


if __name__ == '__main__':
    main()

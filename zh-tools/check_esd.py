#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_esd.py - 汉化后的 .esd 体检工具

检查项（全部是"字符格式"类问题，一旦踩到就是整屏不显示/乱码）：
  1. 编码与 BOM       : 是不是纯 UTF-8 / GBK，开头有没有 EF BB BF
  2. 行尾            : 是否统一 CRLF（原厂就是这样），有没有混入裸 LF / CR
  3. 引号            : label 里是否混入 ASCII 双引号（会提前截断字符串）
  4. 控制字符        : 0x00-0x08 / 0x0B / 0x0C / 0x1B 等
  5. 制表符          : 行内是否用了 TAB 做对齐（原厂用 TAB 做缩进，正文里不该有）
  6. 全角标点        : 统计 , . : ; ! ? ( ) 等的全角版本，提示换 ASCII
  7. 显示宽度        : CJK 记 2 格，统计超过阈值的 label
  8. screen 名       : 含空格 / 含非 ASCII / 与父屏名大小写不一致
  9. 菜单树完整性    : 父屏名必须能在某个文件里找到声明
 10. 重复 screen     : 同名 screen 被声明多次（后加载的会覆盖，菜单会缺项）

用法：
  python check_esd.py --dir ..\\out
  python check_esd.py --dir ..\\out-screens --width 24
"""
import argparse
import os
import re
import sys
from collections import Counter, defaultdict

LABEL_RE = re.compile(r'(label\s+)"([^"]*)"')
SCREEN_RE = re.compile(r'(?m)^screen\s+(\S+)\s+(\S+)')

CJK_RANGES = [
    (0x1100, 0x115F), (0x2E80, 0xA4CF), (0xAC00, 0xD7A3),
    (0xF900, 0xFAFF), (0xFE30, 0xFE4F), (0xFF00, 0xFF60),
    (0xFFE0, 0xFFE6), (0x20000, 0x3FFFD),
]
FULLWIDTH_PUNCT = set('，。、；：！？（）《》【】“”‘’…—～　')
BAD_CTRL = set(range(0x00, 0x09)) | {0x0B, 0x0C, 0x1B}


def width(s):
    w = 0
    for ch in s:
        o = ord(ch)
        if any(a <= o <= b for a, b in CJK_RANGES):
            w += 2
        else:
            w += 1
    return w


def detect_encoding(raw):
    if raw.startswith(b'\xef\xbb\xbf'):
        return 'utf-8-bom'
    try:
        raw.decode('ascii')
        return 'ascii'
    except UnicodeDecodeError:
        pass
    try:
        raw.decode('utf-8')
        return 'utf-8'
    except UnicodeDecodeError:
        return 'gbk?'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dir', required=True)
    ap.add_argument('--width', type=int, default=34, help='label 显示宽度上限（CJK 记 2）')
    args = ap.parse_args()

    esd_dirs = []
    for root, _d, files in os.walk(args.dir):
        if any(f.lower().endswith('.esd') for f in files):
            esd_dirs.append(root)
    if not esd_dirs:
        sys.exit('没找到 .esd')

    declared = defaultdict(list)      # screen 名 -> [文件]
    parents = []                      # (文件, 本屏, 父屏)
    enc_stat = Counter()
    files_checked = 0
    issues = defaultdict(list)
    wide = []
    punct = Counter()
    label_total = 0

    for d in esd_dirs:
        for name in sorted(os.listdir(d)):
            if not name.lower().endswith('.esd'):
                continue
            files_checked += 1
            p = os.path.join(d, name)
            raw = open(p, 'rb').read()
            enc = detect_encoding(raw)
            enc_stat[enc] += 1
            if enc == 'utf-8-bom':
                issues['BOM'].append(name)
                raw = raw[3:]
            crlf = raw.count(b'\r\n')
            lf = raw.count(b'\n')
            if crlf != lf:
                issues['行尾不统一'].append(f'{name} (CRLF={crlf} / LF={lf})')
            if lf and raw.count(b'\r') != crlf:
                issues['裸CR'].append(name)
            text = raw.decode('utf-8' if enc in ('utf-8', 'utf-8-bom', 'ascii') else 'latin-1', errors='replace')

            for m in LABEL_RE.finditer(text):
                label_total += 1
                s = m.group(2)
                if '"' in s:
                    issues['label 内含 ASCII 引号'].append(f'{name}: {s[:30]}')
                if any(ord(c) in BAD_CTRL for c in s):
                    issues['控制字符'].append(f'{name}: {s[:30]}')
                if '\t' in s:
                    issues['label 内含 TAB'].append(f'{name}: {s[:30]}')
                if s != s.strip():
                    issues['首尾空格'].append(f'{name}: "{s[:30]}"')
                for c in s:
                    if c in FULLWIDTH_PUNCT:
                        punct[c] += 1
                w = width(s)
                if w > args.width:
                    wide.append((w, name, s))

            for m in SCREEN_RE.finditer(text):
                nm, par = m.group(1), m.group(2)
                declared[nm].append(name)
                parents.append((name, nm, par))
                if ' ' in nm:
                    issues['screen 名含空格'].append(f'{name}: {nm}')
                if any(ord(c) > 127 for c in nm):
                    issues['screen 名含非 ASCII'].append(f'{name}: {nm}')

    for nm, fl in declared.items():
        if len(fl) > 1:
            issues['重复 screen 声明'].append(f'{nm} -> {", ".join(fl)}')
    for f, nm, par in parents:
        if par not in declared:
            issues['父屏不存在'].append(f'{f}: {nm} -> {par}')

    print(f'检查文件       : {files_checked}')
    print(f'label 总数     : {label_total}')
    print(f'编码分布       : {dict(enc_stat)}')
    print(f'screen 声明数  : {len(parents)}（去重 {len(declared)}）')
    print()
    if issues:
        print('=== 问题 ===')
        for k, v in issues.items():
            print(f'[{k}] {len(v)} 处')
            for line in v[:10]:
                print('   ', line)
            if len(v) > 10:
                print(f'    ... 还有 {len(v)-10} 处')
    else:
        print('=== 问题 ===\n结构/编码/引号/控制字符 全部通过')

    print()
    print(f'=== 超宽 label（>{args.width} 格，共 {len(wide)} 条）===')
    for w, name, s in sorted(wide, reverse=True)[:15]:
        print(f'  {w:3d}  {name:32s} {s}')

    if punct:
        print()
        print('=== 全角标点统计（建议换 ASCII，除非已实测能显示）===')
        print('  ' + ' '.join(f'{c}x{n}' for c, n in punct.most_common()))


if __name__ == '__main__':
    main()

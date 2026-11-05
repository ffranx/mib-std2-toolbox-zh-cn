import hashlib
import os
import zipfile

SRC = r'C:\Users\12321\Documents\deepseek-harness\default-workspace\mib2-zh\out-safe'
DESKTOP = r'C:\Users\12321\Desktop'
ZIPNAME = 'MIB2工具箱-汉化v1.5.1-zh-safe.zip'
ZIP = os.path.join(DESKTOP, ZIPNAME)

# 干净的 zip：所有条目相对 out-safe 根目录，解压出来 metainfo2.txt 直接落在卡根
if os.path.exists(ZIP):
    os.remove(ZIP)

EXCLUDE_TOP = {'.github', '.gitattributes', '.gitignore'}
count = 0
with zipfile.ZipFile(ZIP, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for root, dirs, files in os.walk(SRC):
        dirs.sort()
        for name in sorted(files):
            full = os.path.join(root, name)
            rel = os.path.relpath(full, SRC).replace(os.sep, '/')
            if rel.split('/')[0] in EXCLUDE_TOP:
                continue
            z.write(full, rel)
            count += 1

size = os.path.getsize(ZIP)
h = hashlib.sha256(open(ZIP, 'rb').read()).hexdigest()
print(f'zip   : {ZIP}')
print(f'files : {count}')
print(f'size  : {size/1024/1024:.2f} MB ({size} bytes)')
print(f'sha256: {h}')

# 校验关键内容
with zipfile.ZipFile(ZIP) as z:
    names = z.namelist()
    top = sorted({n.split('/')[0] for n in names})
    print('top-level:', top)
    print('metainfo2.txt 在根:', 'metainfo2.txt' in names)
    probe_utf8 = [n for n in names if n.endswith('zzprobe-utf8.esd')]
    print('探测屏:', probe_utf8)
    sample = [n for n in names if n.endswith('mibstd2-network.esd')][0]
    txt = z.read(sample).decode('utf-8')
    zh = [ln.strip() for ln in txt.splitlines() if 'label' in ln and any('\u4e00' <= c <= '\u9fff' for c in ln)]
    print('sample', sample, '-> 中文 label 行数:', len(zh))
    print('   ', zh[0] if zh else 'NONE')
    bad_bom = [n for n in names if n.endswith('.esd') and z.read(n).startswith(b'\xef\xbb\xbf')]
    print('含 BOM 的 esd:', bad_bom if bad_bom else '无')

# 校验 metainfo2 未被改动
import re
mf = zipfile.ZipFile(ZIP).read('metainfo2.txt').decode('ascii')
ck = re.search(r'MetafileChecksum = "([0-9a-f]{40})"', mf).group(1)
nochk = re.sub(r'(?m)^MetafileChecksum = "[0-9a-f]{40}"\r?\n', '', mf)
pre = nochk[:nochk.index('[Signature]')]
calc = hashlib.sha1(pre.encode('ascii')).hexdigest()
print('metainfo 声明校验 :', ck)
print('metainfo 实算校验 :', calc, '->', 'MATCH' if ck == calc else 'MISMATCH')


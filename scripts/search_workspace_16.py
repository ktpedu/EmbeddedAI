import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

for root, dirs, files in os.walk('.'):
    if any(ig in root for ig in ['.git', 'node_modules', '.gemini']):
        continue
    for fname in files:
        fpath = os.path.join(root, fname)
        try:
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            for m in re.finditer(r'16', content):
                # check context around 16
                start = max(0, m.start() - 30)
                end = min(len(content), m.end() + 30)
                snip = content[start:end].replace('\n', ' ')
                if any(k in snip.lower() for k in ['ep', 'ตอน', 'บทที่ 2', 'ch02', 'youtube', 'video', 'คลิป', 'brick']):
                    print(f"[{fpath}] ...{snip}...")
        except Exception:
            pass

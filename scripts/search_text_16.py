import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

for root, dirs, files in os.walk('.'):
    if any(ig in root for ig in ['.git', 'node_modules', '.gemini']):
        continue
    for fname in files:
        if not fname.endswith(('.md', '.txt', '.json', '.js', '.html')):
            continue
        fpath = os.path.join(root, fname)
        try:
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            # Look for 16 near EP or บท
            for m in re.finditer(r'(?:ep|ตอน|บทที่)[\s\.\-_:]*16\b|16[\s\.\-_:]*(?:ep|ตอน)', content, re.IGNORECASE):
                start = max(0, m.start() - 40)
                end = min(len(content), m.end() + 40)
                print(f"[{fpath}] ...{content[start:end].replace(chr(10), ' ')}...")
        except Exception:
            pass

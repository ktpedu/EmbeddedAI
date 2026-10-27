import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

for i in range(1, 13):
    fname = f'web_learning_platform/public/chapter{i:02d}.html'
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    
    title_m = re.search(r'<title>(.*?)</title>', content)
    title = title_m.group(1).split('|')[0].strip() if title_m else 'No title'
    
    # h1 or hero title
    h1_m = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
    h1 = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', h1_m.group(1))).strip() if h1_m else ''
    
    print(f"File {fname}:")
    print(f"  Title: {title}")
    print(f"  H1: {h1[:100]}")

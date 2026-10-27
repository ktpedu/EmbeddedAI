import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

for ch in range(5, 13):
    fname = f'web_learning_platform/public/chapter{ch:02d}.html'
    with open(fname, 'r', encoding='utf-8') as f:
        c = f.read()
    
    # find first section id
    sec_ids = re.findall(r'<section[^>]+id=[\'"]([^\'"]+)[\'"]', c)
    print(f"CH{ch:02d}: section ids = {sec_ids[:3]}")

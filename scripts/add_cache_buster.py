import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

for ch in range(1, 13):
    ch_str = f"{ch:02d}"
    fpath = f"web_learning_platform/public/chapter{ch_str}.html"
    if not os.path.exists(fpath):
        continue
    with open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    html_new = re.sub(r'src="js/learning-enhancements\.js(?:\?[^"]*)?"', 'src="js/learning-enhancements.js?v=20261017b"', html)
    if html_new != html:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(html_new)
        print(f"Updated cache-buster in chapter{ch_str}.html")

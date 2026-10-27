import os
import re
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

print("=== CHECKING db.json LESSONS ===")
with open('web_learning_platform/data/db.json', 'r', encoding='utf-8') as f:
    db = json.load(f)
for l in db.get('lessons', []):
    print(f"id={l.get('id')}, ch={l.get('chapter')}, video_url={l.get('video_url')}")

print("\n=== CHECKING CHAPTER HTML HERO / HEADER BUTTONS ===")
for i in range(1, 13):
    fname = f'web_learning_platform/public/chapter{i:02d}.html'
    if not os.path.exists(fname):
        print(f'{fname}: NOT FOUND')
        continue
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # check title in header or doc
    title_m = re.search(r'<title>(.*?)</title>', content)
    title = title_m.group(1) if title_m else 'No title'
    
    # chapter progress strip text
    strip_m = re.search(r'<div class="bg-\[#0d2342\].*?</div>\s*</div>', content, re.DOTALL)
    strip_text = "Found" if strip_m else "NOT FOUND"
    
    # youtube links in page
    all_yt = re.findall(r'href=[\'"](https?://[^\'"]*youtu[^\'"]*)[\'"]', content)
    print(f"Ch{i:02d}: strip={strip_text}, yt_links={all_yt}")

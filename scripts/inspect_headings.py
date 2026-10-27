import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

for c in range(1, 13):
    filename = f"web_learning_platform/public/chapter{c:02d}.html"
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()
    
    sections = re.findall(r'<section\s+id="([^"]+)"[^>]*>.*?<h2[^>]*>(.*?)</h2>', html, re.DOTALL)
    print(f"\n==================== Chapter {c:02d} ====================")
    for sid, h2 in sections:
        # clean h2 tags
        h2_clean = re.sub(r'<[^>]+>', '', h2).strip()
        h2_clean = re.sub(r'\s+', ' ', h2_clean)
        print(f"  [{sid}]: {h2_clean[:60]}")

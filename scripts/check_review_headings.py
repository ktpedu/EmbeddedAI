import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

for c in [9, 10, 11, 12]:
    with open(f'web_learning_platform/public/chapter{c:02d}.html', 'r', encoding='utf-8') as f:
        html = f.read()
    m = re.findall(r'<section\s+id="(?:section-review|sec-questions|section-quiz)[^>]*>.*?<h2[^>]*>(.*?)</h2>', html, re.DOTALL)
    print(f"Ch.{c:02d}:", m)

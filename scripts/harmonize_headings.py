import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

for c in [9, 10, 11, 12]:
    filename = f"web_learning_platform/public/chapter{c:02d}.html"
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()
    
    html = html.replace(
        'แบบประเมินและทบทวนความเข้าใจท้ายบทเรียน (Review Questions)',
        'คำถามทบทวนองค์ความรู้ท้ายบทเรียน (Review Questions)'
    )
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Ch.{c:02d}: Harmonized Review Questions heading to match Chapter 1.")

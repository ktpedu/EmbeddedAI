import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('web_learning_platform/public/chapter01.html', 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        if any(k in line for k in ['Ep.', 'Ep ', 'ตอนที่', 'youtube.com', 'youtu.be', 'คลิป']):
            print(f"{idx+1}: {line.strip()[:120]}")

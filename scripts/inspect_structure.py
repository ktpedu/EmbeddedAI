import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/playlist_dump.json', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's inspect where videoId appears
lines = text.splitlines()
for i, line in enumerate(lines):
    if '"videoId":' in line:
        print(f"Around line {i+1}:")
        start = max(0, i-5)
        end = min(len(lines), i+15)
        for j in range(start, end):
            print(f"  {lines[j]}")
        break

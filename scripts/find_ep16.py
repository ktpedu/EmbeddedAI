import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== SEARCHING FOR EP16 / 16 / Video references for Chapter 2 ===")

# 1. Search in web_learning_platform
for root, dirs, files in os.walk('web_learning_platform'):
    if 'node_modules' in root:
        continue
    for fname in files:
        if fname.endswith(('.html', '.js', '.json')):
            fpath = os.path.join(root, fname)
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            # Check for EP 16, Ep.16, EP.16, Ep 16
            for m in re.finditer(r'(?:ep|ตอน|คลิป|video)[\s\.\-_:]*16\b|16[\s\.\-_:]*(?:ep|ตอน)', content, re.IGNORECASE):
                snippet = content[max(0, m.start()-50):min(len(content), m.end()+50)].replace('\n', ' ')
                print(f"[{fpath}] Found pattern: {snippet}")

            # Also check for any mention of chapter 2 with video
            if 'ch02' in content or 'chapter02' in content:
                for m in re.finditer(r'(?:ch02|chapter02)[^\n]{0,100}(?:video|youtube|ep|watch)', content, re.IGNORECASE):
                    snippet = content[max(0, m.start()-30):min(len(content), m.end()+60)].replace('\n', ' ')
                    print(f"[{fpath}] Ch02 video match: {snippet}")

print("\n=== SEARCHING IN SUPABASE / DB.JSON FOR CH02 ===")
import json
with open('web_learning_platform/data/db.json', 'r', encoding='utf-8') as f:
    db = json.load(f)
for l in db.get('lessons', []):
    if l.get('id') == 'ch02' or l.get('chapter_number') == 2:
        print("db.json ch02:", json.dumps(l, ensure_ascii=False, indent=2))

with open('web_learning_platform/data/seed.json', 'r', encoding='utf-8') as f:
    seed = json.load(f)
for l in seed.get('lessons', []):
    if l.get('id') == 'ch02' or l.get('chapter_number') == 2:
        print("seed.json ch02:", json.dumps(l, ensure_ascii=False, indent=2))

import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

for p in ['web_learning_platform/data/db.json', 'web_learning_platform/data/seed.json', 'web_learning_platform/data/db.backup.json']:
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            d = json.load(f)
        lessons = d.get('lessons', [])
        print(f"{p}: has {len(lessons)} lessons")
        if lessons:
            print(f"  first lesson video_url: {lessons[0].get('video_url')}")

import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('web_learning_platform/data/db.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

for l in db['lessons']:
    print(f"{l['id']}: {l['title']}")
    print(f"  video_url: {l.get('video_url')}")
    print(f"  pdf_url: {l.get('pdf_url')}")
    eps = l.get('video_episodes', [])
    if eps:
        print(f"  episodes: {len(eps)}")
        for ep in eps:
            print(f"    - {ep.get('episode')}: {ep.get('title')} ({ep.get('youtube_url')})")

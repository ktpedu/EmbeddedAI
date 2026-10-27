import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/playlist_videos_parsed.json', 'r', encoding='utf-8') as f:
    videos = json.load(f)

for v in videos:
    if any(ep in v['title'] for ep in ['Ep.5', 'Ep. 5', 'Ep.6', 'Ep.7', 'Ep.8', 'Ep.9', 'Ep.10', 'Ep.11', 'Ep.12', 'Ep.13', 'Ep.14']):
        print(f"#{v['index']}: [{v['videoId']}] {v['title']} ({v['duration']})")

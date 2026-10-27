import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/playlist_videos_parsed.json', 'r', encoding='utf-8') as f:
    videos = json.load(f)

for v in videos:
    if any(k in v['title'] for k in ['11', '12', '13', '14']):
        print(f"#{v['index']}: [{v['videoId']}] {v['title']} ({v['duration']})")

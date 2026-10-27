import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/playlist_videos_parsed.json', 'r', encoding='utf-8') as f:
    videos = json.load(f)

print(f"Total videos: {len(videos)}")
for v in videos[:40]:
    print(f"#{v['index']}: [{v['videoId']}] {v['title']} ({v['duration']})")

import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/playlist_dump.json', 'r', encoding='utf-8') as f:
    text = f.read()

# Match videoId
vids = re.findall(r'"videoId":\s*"([^"]+)"', text)
print(f"Total videoId occurrences: {len(vids)}")

# Look for titles
# In indented JSON:
# "playlistVideoRenderer": {
#   "videoId": "xyz",
#   ...
#   "title": {
#     "runs": [
#       {
#         "text": "title here"
#       }
#     ]

# Let's use json.loads instead of regex!
data = json.loads(text)

videos = []

def walk(node):
    if isinstance(node, dict):
        if 'playlistVideoRenderer' in node:
            vr = node['playlistVideoRenderer']
            vid = vr.get('videoId')
            # Extract title
            title = ''
            if 'title' in vr:
                runs = vr['title'].get('runs', [])
                if runs:
                    title = runs[0].get('text', '')
                elif 'simpleText' in vr['title']:
                    title = vr['title']['simpleText']
            idx = vr.get('index', {}).get('simpleText', '')
            length = vr.get('lengthText', {}).get('simpleText', '')
            videos.append({
                'index': idx,
                'videoId': vid,
                'title': title,
                'length': length
            })
        else:
            for v in node.values():
                walk(v)
    elif isinstance(node, list):
        for item in node:
            walk(item)

walk(data)

print(f"Total videos parsed via walk: {len(videos)}")
for v in videos:
    print(f"#{v['index']}: [{v['videoId']}] {v['title']} ({v['length']})")

with open('scripts/playlist_videos.json', 'w', encoding='utf-8') as f:
    json.dump(videos, f, ensure_ascii=False, indent=2)

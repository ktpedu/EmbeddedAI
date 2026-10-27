import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

res = urllib.request.urlopen('http://localhost:3001/api/lessons')
data = json.loads(res.read().decode('utf-8'))
for l in data['data']:
    print(f"Chapter {l.get('chapter_number')}: id={l.get('id')} video_url={l.get('video_url')} slide_url={l.get('slide_url')}")
    if 'video_episodes' in l:
        print(f"   -> episodes: {len(l['video_episodes'])} episodes")

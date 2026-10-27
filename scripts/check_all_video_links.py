import urllib.request
import re
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Let's inspect the playlist or db.json video list
with open('web_learning_platform/data/db.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

lessons = db.get('lessons', [])
all_vids = []
for lesson in lessons:
    ch = lesson.get('id')
    # check video_url
    vurl = lesson.get('video_url', '')
    if vurl:
        all_vids.append((ch, 'main', vurl))
    # check video_episodes
    eps = lesson.get('video_episodes', [])
    for ep in eps:
        all_vids.append((ch, ep.get('episode', ''), ep.get('youtube_url', '')))

print(f"Total video entries found in db.json: {len(all_vids)}")

results = []
for ch, ep, vurl in all_vids:
    vid_m = re.search(r'(?:v=|youtu\.be/)([\w-]{11})', vurl)
    if not vid_m:
        continue
    vid = vid_m.group(1)
    req = urllib.request.Request(f"https://www.youtube.com/watch?v={vid}", headers={'User-Agent': 'Mozilla/5.0'})
    try:
        html = urllib.request.urlopen(req, timeout=8).read().decode('utf-8', errors='ignore')
        box_links = list(set(re.findall(r'https?://(?:app\.)?box\.com/[^\s"\'<>]+', html)))
        desc_m = re.search(r'"shortDescription":"(.*?)"', html)
        desc_text = ''
        if desc_m:
            try:
                desc_text = desc_m.group(1).encode('utf-8').decode('unicode_escape')
            except Exception:
                desc_text = desc_m.group(1)
        # find any other URLs in desc
        all_urls = list(set(re.findall(r'https?://[^\s"\'<>\\]+', desc_text)))
        results.append({
            'chapter': ch,
            'ep': ep,
            'vid': vid,
            'box_links': box_links,
            'all_urls': all_urls,
            'desc_snippet': desc_text[:120]
        })
        print(f"Ch.{ch} ({ep}) [{vid}]: Box: {box_links} | Other: {all_urls}")
    except Exception as e:
        print(f"Error {ch} {vid}: {e}")

with open('scripts/all_video_links.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print("Saved to scripts/all_video_links.json")

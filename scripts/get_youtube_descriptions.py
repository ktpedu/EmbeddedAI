import urllib.request
import re
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

video_ids = [
    ('Ep.01', 'oVg57hOrU4s'),
    ('Ep.02', 'IUrO0bfUvc0'),
    ('Ep.03', 'cRO5jjGtE_k'),
    ('Ep.04', 'nO3FicIusQs'),
    ('Ep.29', '-X8y_aeMAFY')
]

for ep, vid in video_ids:
    url = f"https://www.youtube.com/watch?v={vid}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8', errors='ignore')
        box_links = re.findall(r'https?://[^\s"\'<>]*box\.com[^\s"\'<>]*', html)
        title_m = re.search(r'<title>(.*?)</title>', html)
        title = title_m.group(1) if title_m else ''
        print(f"=== {ep}: {vid} | {title} ===")
        # search all links in description
        desc_m = re.search(r'"shortDescription":"(.*?)"', html)
        if desc_m:
            desc = desc_m.group(1).encode('utf-8').decode('unicode_escape')
            print("Description:")
            print(desc)
            print("-" * 50)
        else:
            print("Box links found:", set(box_links))
    except Exception as e:
        print(f"Error {ep} {vid}:", e)

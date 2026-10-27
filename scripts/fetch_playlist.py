import urllib.request
import re
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

playlist_url = 'https://www.youtube.com/playlist?list=PL_P41WM_1HxGmyUuNPQQsDa-ItaDu5VyU'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'th,en-US;q=0.9,en;q=0.8'
}

req = urllib.request.Request(playlist_url, headers=headers)
try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8')
        
    print(f"Fetched playlist page, size: {len(html)}")
    
    # Extract ytInitialData
    match = re.search(r'var ytInitialData\s*=\s*({.+?});</script>', html)
    if not match:
        match = re.search(r'window\["ytInitialData"\]\s*=\s*({.+?});', html)
        
    if match:
        data = json.loads(match.group(1))
        # Navigate to playlist items
        # Usually: contents -> twoColumnBrowseResultsRenderer -> tabs -> ...
        with open('scripts/playlist_dump.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("Saved ytInitialData to scripts/playlist_dump.json")
    else:
        print("Could not find ytInitialData in page")
        with open('scripts/playlist_page.html', 'w', encoding='utf-8') as f:
            f.write(html)
except Exception as e:
    print("Error fetching playlist:", e)

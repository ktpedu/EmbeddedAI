import urllib.request
import urllib.parse
import re
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

def search_yt(query):
    url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'th,en-US;q=0.9,en;q=0.8'
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8')
        m = re.findall(r'"videoId":\s*"([^"]+)".*?"title":\s*\{\s*"runs":\s*\[\s*\{\s*"text":\s*"([^"]+)"', html)
        print(f"Results for '{query}': {len(m)}")
        seen = set()
        for vid, title in m:
            if vid not in seen:
                seen.add(vid)
                print(f"  [{vid}] {title}")
    except Exception as e:
        print(f"Error searching '{query}':", e)

search_yt('Arduino UNO Q Ep.11 ธนา')
search_yt('Arduino UNO Q Ep.12 ธนา')
search_yt('Arduino UNO Q Ep.13 ธนา')
search_yt('Arduino UNO Q Ep.14 ธนา')

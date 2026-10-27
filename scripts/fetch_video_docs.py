import urllib.request
import re
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

# List of key video IDs across chapters
video_map = {
    # Chapter 1
    'ch01_ep01': 'oVg57hOrU4s',
    'ch01_ep02': 'IUrO0bfUvc0',
    'ch01_ep03': 'cRO5jjGtE_k',
    'ch01_ep04': 'nO3FicIusQs',
    
    # Chapter 2
    'ch02_ep05': 'g4sF5nnsSeY',
    'ch02_ep06': 'DVCrb6t5dls',
    'ch02_ep07': 'zu6CBc-GZpM',
    'ch02_ep08': 'pcw_iF02Ros',
    'ch02_ep09': '7JBtwM5m-YI',
    'ch02_ep10': '36Z_RYn6pQI',
    
    # Chapter 3 (Database-SQL)
    'ch03_ep16': 'N-tZirbAWCE',
    'ch03_ep17': 'MekwqhTuTzc',
    
    # Chapter 4 (Edge Impulse)
    'ch04_ep29': '-X8y_aeMAFY',
    
    # Chapter 5 (FOMO-AD)
    'ch05_ep30': '1yEMEJnsrUY',
    
    # Chapter 6 (.eim Deploy)
    'ch06_ep33': '3mAwLsQjv6U',
    'ch06_ep35': '0g2F-s-7O2U',
    
    # Chapter 7 (VAD & DB)
    'ch07_ep34': '5Xiz_W53yU0',
    
    # Chapter 8 (FOMO Object Detection)
    'ch08_ep31': 'glQx9GTLEUI',
    'ch08_ep18': 'mkmYqMgfaUw',
    
    # Chapter 9 (Actuator)
    'ch09_ep42': '6DlVYQzgrEw',
    
    # Chapter 10 (Image Classification)
    'ch010_ep32': '3EmkC1QBZK0',
    'ch010_ep43': 'bLw9BH5RrFo',
    
    # Chapter 11 (KWS)
    'ch011_ep44': 'CRpBHlDRh60',
    'ch011_ep36': 'Lt5RQeWXZBA',
    
    # Chapter 12 (Audio Classification)
    'ch012_ep45': 'OSzculUyvaY',
    'ch012_ep39': '9R-vpS6F4jA',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'th,en-US;q=0.9,en;q=0.8'
}

results = {}

for label, vid in video_map.items():
    url = f"https://www.youtube.com/watch?v={vid}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8')
            
        # Extract title
        title_match = re.search(r'<title>(.*?)</title>', html)
        title = title_match.group(1).replace(' - YouTube', '') if title_match else ''
        
        # Extract Box links
        # Box URLs look like https://app.box.com/s/3gl7jnelf5uj39csjocopzsphuc8i0pu
        box_links = list(set(re.findall(r'https?://(?:app\.)?box\.com/s/[a-zA-Z0-9_-]+', html)))
        
        # Also find all URLs in description
        all_urls = list(set(re.findall(r'https?://[^\s"<>\\]+', html)))
        # Filter relevant URLs (box, github, drive, etc.)
        doc_urls = [u for u in all_urls if any(d in u for d in ['box.com', 'github.com', 'drive.google'])]
        
        results[label] = {
            'vid': vid,
            'title': title,
            'box_links': box_links,
            'doc_urls': doc_urls[:5]
        }
        print(f"[{label}] ({vid}) -> Box: {box_links}")
    except Exception as e:
        print(f"[{label}] ({vid}) -> Error: {e}")

with open('scripts/extracted_video_docs.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("\nDone! Saved to scripts/extracted_video_docs.json")

import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/playlist_dump.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

videos = []

def extract_lockups(node):
    if isinstance(node, dict):
        if 'lockupViewModel' in node:
            lm = node['lockupViewModel']
            # extract title
            title = ''
            title_node = lm.get('metadata', {}).get('lockupMetadataViewModel', {}).get('title', {})
            title = title_node.get('content', '')
            
            # extract videoId
            vid = ''
            # Search for videoId in node
            node_str = json.dumps(lm)
            import re
            m = re.search(r'"videoId":\s*"([^"]+)"', node_str)
            if m:
                vid = m.group(1)
                
            # duration
            dur = ''
            m_dur = re.search(r'"thumbnailBadgeViewModel":\s*\{\s*"text":\s*"([^"]+)"', node_str)
            if m_dur:
                dur = m_dur.group(1)

            if vid and title:
                videos.append({
                    'index': len(videos) + 1,
                    'videoId': vid,
                    'title': title,
                    'duration': dur
                })
        else:
            for v in node.values():
                extract_lockups(v)
    elif isinstance(node, list):
        for item in node:
            extract_lockups(item)

extract_lockups(data)

print(f"Total videos extracted from playlist: {len(videos)}")
for v in videos:
    print(f"#{v['index']}: [{v['videoId']}] {v['title']} ({v['duration']})")

with open('scripts/playlist_videos_parsed.json', 'w', encoding='utf-8') as f:
    json.dump(videos, f, ensure_ascii=False, indent=2)

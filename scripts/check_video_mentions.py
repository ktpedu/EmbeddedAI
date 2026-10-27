import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

for ch in range(5, 13):
    fname = f'web_learning_platform/public/chapter{ch:02d}.html'
    with open(fname, 'r', encoding='utf-8') as f:
        c = f.read()
    
    # search for youtube or video mentions
    yt_mentions = re.findall(r'(https?://[^\s"\'<>]*youtu[^\s"\'<>]*)', c)
    iframe_mentions = re.findall(r'<iframe[^>]*src=[\'"]([^\'"]+)[\'"]', c)
    print(f"CH{ch:02d}: YT links = {len(yt_mentions)}, iframes = {len(iframe_mentions)}")
    if yt_mentions:
        print("  YT links:", yt_mentions)
    if iframe_mentions:
        print("  iframes:", iframe_mentions)

import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

for ch in range(5, 13):
    fname = f'web_learning_platform/public/chapter{ch:02d}.html'
    with open(fname, 'r', encoding='utf-8') as f:
        c = f.read()
    
    # find hero section
    m = re.search(r'(<section class="bg-gradient-to-r.*?</section>)', c, re.DOTALL)
    if m:
        hero = m.group(1)
        print(f"=== CH{ch:02d} HERO ===")
        # find p tag in hero
        p_m = re.findall(r'<p[^>]*>.*?</p>', hero, re.DOTALL)
        for p in p_m:
            print("  P:", re.sub(r'\s+', ' ', p)[:100])
        print("  Length:", len(hero))

import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

for ch in range(5, 13):
    fname = f'web_learning_platform/public/chapter{ch:02d}.html'
    with open(fname, 'r', encoding='utf-8') as f:
        c = f.read()
    
    # find hero section
    hero_m = re.search(r'(<section class="bg-gradient-to-r.*?</section>)', c, re.DOTALL)
    if not hero_m:
        print(f"CH{ch:02d}: Hero not found!")
        continue
    hero = hero_m.group(1)
    
    # find where meta card begins
    meta_m = re.search(r'(<!--\s*(?:Quick\s*)?(?:Lesson\s*)?Meta\s*Card\s*-->)', hero, re.IGNORECASE)
    if meta_m:
        print(f"CH{ch:02d}: Found Meta Card marker! Preceding 150 chars:")
        st = max(0, meta_m.start() - 150)
        print(repr(hero[st:meta_m.start()]))
    else:
        print(f"CH{ch:02d}: Meta Card marker not found!")

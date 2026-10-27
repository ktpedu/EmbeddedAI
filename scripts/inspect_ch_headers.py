import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

for i in range(1, 13):
    fname = f'web_learning_platform/public/chapter{i:02d}.html'
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"=== CH{i:02d} ===")
    header_m = re.search(r'<header.*?</header>', content, re.DOTALL)
    if header_m:
        header_links = re.findall(r'href=[\'"]([^\'"]*youtu[^\'"]*)[\'"]', header_m.group(0))
        print('  Header YT:', header_links)
        
        # Check title in strip
        strip_title_m = re.search(r'<span class="font-semibold text-white truncate">(.*?)</span>', header_m.group(0))
        if strip_title_m:
            print('  Strip Title:', strip_title_m.group(1))
    
    hero_m = re.search(r'<section class="bg-gradient-to-r.*?</section>', content, re.DOTALL)
    if hero_m:
        hero_links = re.findall(r'href=[\'"]([^\'"]*youtu[^\'"]*)[\'"]', hero_m.group(0))
        print('  Hero YT:', hero_links)

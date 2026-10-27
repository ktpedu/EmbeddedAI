import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

for i in range(5, 13):
    fname = f'web_learning_platform/public/chapter{i:02d}.html'
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    
    header_m = re.search(r'(<!-- =+ -->\s*<!-- 2\. MAIN NAVIGATION BAR.*?<!-- =+ -->\s*<!-- 3\. CHAPTER HERO BANNER)', content, re.DOTALL)
    if header_m:
        print(f"=== CH{i:02d} Navigation block ===")
        print(header_m.group(1)[:300])
        print("...")
        print(header_m.group(1)[-200:])
    else:
        print(f"=== CH{i:02d} Nav block pattern not matched! ===")
        m2 = re.search(r'<header.*?</header>', content, re.DOTALL)
        if m2:
            print("Found header tag:", m2.group(0)[:150])

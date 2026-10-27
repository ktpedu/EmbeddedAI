import os
import re
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

print("=" * 70)
print("VERIFICATION OF CHAPTER HTML HEADERS AND VIDEO LINKS (CH 01 - 12)")
print("=" * 70)

all_ok = True

for i in range(1, 13):
    fname = f'web_learning_platform/public/chapter{i:02d}.html'
    with open(fname, 'r', encoding='utf-8') as f:
        c = f.read()
    
    header_m = re.search(r'<header.*?</header>', c, re.DOTALL)
    if not header_m:
        print(f"[FAIL] Ch{i:02d}: No header tag!")
        all_ok = False
        continue
    
    hdr = header_m.group(0)
    has_back = 'กลับสารบัญบทเรียน' in hdr
    has_yt_btn = 'สื่อวีดิทัศน์ประกอบการจัดการเรียนรู้' in hdr
    
    # Extract header video link
    header_yt = re.findall(r'href=[\'"]([^\'"]*youtu[^\'"]*)[\'"]', hdr)
    header_yt_link = header_yt[0] if header_yt else 'NONE'
    
    # Extract strip title
    strip_m = re.search(r'<span class="font-semibold text-white truncate">(.*?)</span>', hdr)
    strip_title = strip_m.group(1) if strip_m else 'NONE'
    
    # Extract hero video link
    hero_m = re.search(r'<section class="bg-gradient-to-r.*?</section>', c, re.DOTALL)
    hero_yt = []
    if hero_m:
        hero_yt = re.findall(r'href=[\'"]([^\'"]*youtu[^\'"]*)[\'"]', hero_m.group(0))
    hero_yt_link = hero_yt[0] if hero_yt else 'NONE'
    
    status = "OK" if has_back and has_yt_btn and header_yt_link != 'NONE' and hero_yt_link != 'NONE' else "FAIL"
    if status == "FAIL":
        all_ok = False
    
    print(f"Ch{i:02d} [{status}]:")
    print(f"  Back Btn   : {has_back}")
    print(f"  YT Header  : {header_yt_link}")
    print(f"  YT Hero    : {hero_yt_link}")
    print(f"  Strip Title: {strip_title}")

print("\n" + "=" * 70)
print("VERIFICATION OF db.json LESSONS")
print("=" * 70)
with open('web_learning_platform/data/db.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

for l in db.get('lessons', []):
    print(f"{l.get('id')}: ch_num={l.get('chapter_number')}, video={l.get('video_url')}")

print("\nOVERALL STATUS:", "ALL TESTS PASSED!" if all_ok else "SOME TESTS FAILED!")

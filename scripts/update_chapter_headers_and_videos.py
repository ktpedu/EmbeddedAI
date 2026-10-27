#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script: update_chapter_headers_and_videos.py
Description:
1. Standardizes <header> and chapter progress strip across chapter05.html - chapter12.html
   to match chapter04.html, adding:
   - [← กลับสารบัญบทเรียน] button
   - [ สื่อวีดิทัศน์ประกอบการจัดการเรียนรู้ ] YouTube red button
   - Sub-strip banner with chapter badge, chapter title, and class duration
2. Adds Hero Quick Action Buttons (เริ่มต้นศึกษาเนื้อหา, สื่อวีดิทัศน์ประจำบทเรียน, เอกสาร PDF)
3. Standardizes Top Utility Bar
4. Updates specific YouTube video URLs across all chapters 1 - 12 (HTML & db.json / seed.json / db.backup.json)
"""

import os
import sys
import re
import json

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC_DIR = os.path.join(ROOT_DIR, 'web_learning_platform', 'public')
DATA_DIR = os.path.join(ROOT_DIR, 'web_learning_platform', 'data')

BOX_PDF_URL = "https://app.box.com/s/3gl7jnelf5uj39csjocopzsphuc8i0pu"

CHAPTER_CONFIG = {
    1: {
        "title": "การเตรียมความพร้อมระบบและบอร์ดพัฒนา Arduino UNO Q",
        "video_url": "https://www.youtube.com/watch?v=-X8y_aeMAFY&t=52s",
        "first_sec": "section-ep1"
    },
    2: {
        "title": "สถาปัตยกรรมซอฟต์แวร์แบบมอดูล (Modular Brick) และการควบคุมฮาร์ดแวร์พื้นฐาน",
        "video_url": "https://youtube.com/playlist?list=PL_P41WM_1HxGmyUuNPQQsDa-ItaDu5VyU",
        "first_sec": "section-ep1"
    },
    3: {
        "title": "การจัดการระบบฐานข้อมูลบนอุปกรณ์ด้วย Database-SQL Brick",
        "video_url": "https://youtube.com/playlist?list=PL_P41WM_1HxGmyUuNPQQsDa-ItaDu5VyU",
        "first_sec": "section-ep1"
    },
    4: {
        "title": "การจัดเตรียมชุดข้อมูลและการออกแบบขั้นตอนการประมวลผล (Data Pipeline) บน Edge Impulse",
        "video_url": "https://www.youtube.com/watch?v=-X8y_aeMAFY&t=52s",
        "first_sec": "section-ep1"
    },
    5: {
        "title": "การฝึกสอนโมเดลตรวจจับความผิดปกติจากภาพ (Visual Anomaly Detection)",
        "video_url": "https://www.youtube.com/watch?v=1yEMEJnsrUY",
        "first_sec": "sec-objectives"
    },
    6: {
        "title": "การนำโมเดล .eim ไปใช้งานและการกำหนดค่าไฟล์ app.yaml บนบอร์ดพัฒนา Arduino UNO Q",
        "video_url": "https://www.youtube.com/watch?v=3mAwLsQjv6U&list=PL_P41WM_1HxGmyUuNPQQsDa-ItaDu5VyU&index=31",
        "first_sec": "sec-objectives"
    },
    7: {
        "title": "การประมวลผลโมเดลตรวจจับความผิดปกติจากภาพ และการบันทึกข้อมูลลง Database-SQL Brick",
        "video_url": "https://www.youtube.com/watch?v=5Xiz_W53yU0&list=PL_P41WM_1HxGmyUuNPQQsDa-ItaDu5VyU&index=33",
        "first_sec": "sec-objectives"
    },
    8: {
        "title": "การฝึกสอนโมเดลตรวจจับวัตถุด้วยสถาปัตยกรรม FOMO (Object Detection)",
        "video_url": "https://www.youtube.com/watch?v=glQx9GTLEUI&list=PL_P41WM_1HxGmyUuNPQQsDa-ItaDu5VyU&index=30",
        "first_sec": "sec-objectives"
    },
    9: {
        "title": "การนำโมเดล FOMO ไปใช้งานและการควบคุมอุปกรณ์ขับเคลื่อน (Actuator)",
        "video_url": "https://www.youtube.com/watch?v=6DlVYQzgrEw&list=PL_P41WM_1HxGmyUuNPQQsDa-ItaDu5VyU&index=41",
        "first_sec": "section-objectives"
    },
    10: {
        "title": "การพัฒนาและประมวลผลโมเดลจำแนกประเภทภาพ (Image Classification)",
        "video_url": "https://www.youtube.com/watch?v=3EmkC1QBZK0&list=PL_P41WM_1HxGmyUuNPQQsDa-ItaDu5VyU&index=32",
        "first_sec": "section-objectives"
    },
    11: {
        "title": "การประมวลผลสัญญาณเสียงและการฝึกสอนโมเดลรู้จำคำสั่งเสียง (Keyword Spotting: KWS)",
        "video_url": "https://www.youtube.com/watch?v=CRpBHlDRh60&list=PL_P41WM_1HxGmyUuNPQQsDa-ItaDu5VyU&index=43",
        "first_sec": "section-objectives"
    },
    12: {
        "title": "การจำแนกเสียงเฉพาะทางและการบูรณาการระบบ Edge AI เชิงวิศวกรรม",
        "video_url": "https://www.youtube.com/watch?v=OSzculUyvaY&list=PL_P41WM_1HxGmyUuNPQQsDa-ItaDu5VyU&index=44",
        "first_sec": "section-objectives"
    }
}

NEW_HEADER_TEMPLATE = """  <!-- ============================================================== -->
  <!-- 2. MAIN HEADER (depa THEME)                                    -->
  <!-- ============================================================== -->
  <header class="bg-[#173b6b] text-white shadow-xl sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-20">
        
        <!-- KT-Edu Logo & Title -->
        <a href="index.html" class="flex items-center space-x-3.5 hover:opacity-95 transition">
          <img src="images/logo/logo_kt_edu.png" alt="KT-Edu" class="h-12 w-12 sm:h-14 sm:w-14 object-contain rounded-full shadow-lg border-2 border-[#fff200] bg-black p-0.5">
          <div>
            <div class="font-bold text-base sm:text-lg leading-tight">
              <span class="text-white font-heading font-extrabold tracking-tight">ปัญญาประดิษฐ์บนระบบสมองกลฝังตัว</span>
            </div>
            <div class="text-xs text-yellow-200/90 font-mono tracking-wider flex items-center gap-1.5 mt-0.5">
              <span>Embedded AI • Arduino UNO Q • Edge Impulse</span>
            </div>
          </div>
        </a>

        <!-- Header Action Buttons -->
        <div class="flex items-center space-x-3">
          <a href="index.html#section-lessons" class="hidden sm:inline-flex items-center gap-2 bg-white/10 hover:bg-white/20 text-white px-4 py-2 rounded-xl text-xs sm:text-sm font-bold border border-white/20 transition">
            <i class="fa-solid fa-arrow-left"></i> กลับสารบัญบทเรียน
          </a>
          <a href="{video_url}" target="_blank" class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-xl text-xs sm:text-sm font-bold shadow flex items-center gap-2 transition">
            <i class="fa-brands fa-youtube"></i> <span class="hidden md:inline">สื่อวีดิทัศน์ประกอบการจัดการเรียนรู้</span>
          </a>
        </div>

      </div>
    </div>

    <!-- Chapter Progress Strip -->
    <div class="bg-[#0d2342] border-t border-white/10 px-4 sm:px-6 lg:px-8 py-2">
      <div class="max-w-7xl mx-auto flex items-center justify-between text-xs text-slate-300">
        <div class="flex items-center space-x-2 flex-shrink-0">
          <span class="bg-[#fff200] text-[#173b6b] font-black px-2 py-0.5 rounded text-[11px]">บทเรียนที่ {ch_num}</span>
          <span class="font-semibold text-white truncate">{ch_title}</span>
        </div>
        <div class="flex items-center space-x-3 text-[11px] font-medium">
          <span class="text-yellow-300"><i class="fa-regular fa-clock mr-1"></i>เวลาเรียน 3 คาบ (150 นาที)</span>
        </div>
      </div>
    </div>
  </header>"""

TOP_UTILITY_BAR = """  <!-- ============================================================== -->
  <!-- 1. TOP UTILITY BAR                                             -->
  <!-- ============================================================== -->
  <div class="bg-[#0d2342] text-slate-300 text-xs py-1.5 px-4 sm:px-6 lg:px-8 border-b border-white/10 hidden md:block">
    <div class="max-w-7xl mx-auto flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <span class="text-yellow-300 font-semibold flex items-center gap-1.5">
          <i class="fa-solid fa-bolt text-[#fff200]"></i> KT-Edu Learning Module
        </span>
        <span class="text-white/30">|</span>
        <span class="text-slate-300">คู่มือบทเรียนฉบับสมบูรณ์ รายวิชาปัญญาประดิษฐ์บนระบบสมองกลฝังตัว</span>
      </div>
      <div class="flex items-center space-x-4">
        <!-- Font resizer -->
        <div class="flex items-center space-x-1">
          <span class="text-slate-400 mr-1">ขนาดอักษร:</span>
          <button onclick="changeFontSize(-1)" class="px-1.5 py-0.5 rounded hover:bg-white/10 text-[11px]">A-</button>
          <button onclick="changeFontSize(0)" class="px-1.5 py-0.5 rounded hover:bg-white/10 text-xs font-bold text-yellow-300">A</button>
          <button onclick="changeFontSize(1)" class="px-1.5 py-0.5 rounded hover:bg-white/10 text-sm font-bold">A+</button>
        </div>
        <span class="text-white/20">|</span>
        <!-- Google Font Switcher -->
        <div class="flex items-center space-x-1">
          <span class="text-slate-400 mr-1"><i class="fa-brands fa-google text-[#fff200] mr-1"></i>ฟอนต์:</span>
          <button onclick="setFontStyle('noto')" id="fontBtn-noto" class="px-2 py-0.5 rounded text-[11px] font-bold bg-[#fff200] text-[#173b6b] shadow transition" title="Google Noto Sans Thai">Google Noto</button>
          <button onclick="setFontStyle('prompt')" id="fontBtn-prompt" class="px-2 py-0.5 rounded text-[11px] text-slate-300 hover:text-white hover:bg-white/10 transition" title="Prompt">Prompt</button>
          <button onclick="setFontStyle('sarabun')" id="fontBtn-sarabun" class="px-2 py-0.5 rounded text-[11px] text-slate-300 hover:text-white hover:bg-white/10 transition" title="สารบรรณ">สารบรรณ</button>
        </div>
        <span class="text-white/20">|</span>
        <a href="https://www.facebook.com/profile.php?id=61595550414518" target="_blank" class="text-slate-300 hover:text-yellow-300 flex items-center gap-1 font-semibold text-xs transition" title="เพจ Facebook ของฉัน"><i class="fa-brands fa-facebook-f text-[#1877f2]"></i> <span class="hidden sm:inline">เพจของฉัน</span></a>
        <span class="text-white/20">|</span>
        <a href="index.html" class="text-yellow-300 hover:text-white flex items-center gap-1 font-semibold text-xs">
          <i class="fa-solid fa-house text-xs"></i> หน้าหลักแพลตฟอร์ม
        </a>
      </div>
    </div>
  </div>"""

def generate_hero_buttons(first_sec, video_url):
    return f"""
        <!-- Quick Action Buttons -->
        <div class="flex flex-wrap gap-3 pt-3">
          <a href="#{first_sec}" class="btn-depa-yellow px-5 py-2.5 rounded-xl text-xs sm:text-sm font-bold shadow-lg flex items-center gap-2">
            <i class="fa-solid fa-book-open"></i> เริ่มต้นศึกษาเนื้อหา
          </a>
          <a href="{video_url}" target="_blank" class="bg-white/10 hover:bg-white/20 text-white border border-white/30 px-5 py-2.5 rounded-xl text-xs sm:text-sm font-bold flex items-center gap-2 transition">
            <i class="fa-brands fa-youtube text-red-400 text-base"></i> สื่อวีดิทัศน์ประจำบทเรียน
          </a>
          <a href="{BOX_PDF_URL}" target="_blank" class="bg-blue-600/70 hover:bg-blue-600 text-white px-4 py-2.5 rounded-xl text-xs sm:text-sm font-bold flex items-center gap-2 transition">
            <i class="fa-solid fa-file-pdf"></i> เอกสารประกอบการบรรยาย (PDF)
          </a>
        </div>"""

def update_html_chapter(ch_num):
    fname = os.path.join(PUBLIC_DIR, f"chapter{ch_num:02d}.html")
    if not os.path.exists(fname):
        print(f"[!] File not found: {fname}")
        return False
    
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    
    cfg = CHAPTER_CONFIG[ch_num]
    video_url = cfg["video_url"]
    ch_title = cfg["title"]
    first_sec = cfg["first_sec"]
    
    # 1. Update Chapters 5-12 (replace old header and add hero buttons)
    if ch_num >= 5:
        # Standardize Top Utility Bar
        top_bar_pattern = re.compile(r'<!-- =+ -->\s*<!-- 1\. TOP UTILITY BAR.*?<!-- =+ -->\s*<!-- 2\. MAIN', re.DOTALL)
        if top_bar_pattern.search(content):
            content = top_bar_pattern.sub(f'{TOP_UTILITY_BAR}\n\n  <!-- ============================================================== -->\n  <!-- 2. MAIN', content)
        
        # Replace <header ...>...</header>
        new_header = NEW_HEADER_TEMPLATE.format(
            video_url=video_url,
            ch_num=ch_num,
            ch_title=ch_title
        )
        header_pattern = re.compile(r'<header.*?</header>', re.DOTALL)
        content = header_pattern.sub(new_header.strip(), content, count=1)
        
        # Insert Hero Quick Action Buttons if not already present
        if 'สื่อวีดิทัศน์ประจำบทเรียน' not in content:
            hero_buttons_html = generate_hero_buttons(first_sec, video_url)
            # Find the closing </p> before Meta Card in hero
            # E.g. </p>\s*</div>\s*(?:<!--\s*(?:Quick\s*)?(?:Lesson\s*)?Meta\s*Card)
            p_close_pattern = re.compile(r'(</p>)(\s*</div>\s*<!--\s*(?:Quick\s*)?(?:Lesson\s*)?Meta\s*Card)', re.DOTALL | re.IGNORECASE)
            if p_close_pattern.search(content):
                content = p_close_pattern.sub(r'\1' + hero_buttons_html + r'\2', content, count=1)
            else:
                print(f"[!] Warning: Could not find hero insertion point for Ch{ch_num}")
        else:
            # Update existing hero video link
            content = re.sub(
                r'(<a\s+href=")[^"]*("\s+target="_blank"\s+class="[^"]*">\s*<i\s+class="fa-brands\s+fa-youtube[^"]*"></i>\s*สื่อวีดิทัศน์ประจำบทเรียน)',
                rf'\g<1>{video_url}\g<2>',
                content
            )

    # 2. Update Chapters 1-4 (ensure video link in header and hero matches exact specific video)
    else:
        # Update header video URL
        content = re.sub(
            r'(<header.*?)href="https?://[^"]*youtu[^"]*"( target="_blank" class="bg-red-600.*?</header>)',
            rf'\g<1>href="{video_url}"\g<2>',
            content,
            flags=re.DOTALL
        )
        # Update hero video URL
        content = re.sub(
            r'(<a\s+href=")[^"]*("\s+target="_blank"\s+class="[^"]*">\s*<i\s+class="fa-brands\s+fa-youtube[^"]*"></i>\s*สื่อวีดิทัศน์ประจำบทเรียน)',
            rf'\g<1>{video_url}\g<2>',
            content
        )

    with open(fname, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[OK] Successfully updated chapter{ch_num:02d}.html")
    return True

def update_database_files():
    json_files = [
        os.path.join(DATA_DIR, 'db.json'),
        os.path.join(DATA_DIR, 'seed.json'),
        os.path.join(DATA_DIR, 'db.backup.json')
    ]
    
    for jf in json_files:
        if not os.path.exists(jf):
            print(f"[!] File not found: {jf}")
            continue
        with open(jf, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        lessons = data.get('lessons', [])
        updated_count = 0
        for l in lessons:
            ch_num = l.get('chapter_number')
            if not ch_num:
                # Try parsing from id, e.g., 'ch01'
                id_str = l.get('id', '')
                m = re.search(r'\d+', id_str)
                if m:
                    ch_num = int(m.group(0))
            
            if ch_num and ch_num in CHAPTER_CONFIG:
                cfg = CHAPTER_CONFIG[ch_num]
                l['video_url'] = cfg['video_url']
                l['title'] = cfg['title']
                updated_count += 1
        
        with open(jf, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"[OK] Updated {updated_count} lessons in {os.path.basename(jf)}")

if __name__ == '__main__':
    print("=" * 60)
    print("Updating Chapter HTML Headers & Videos (Ch 01 - 12)")
    print("=" * 60)
    for ch in range(1, 13):
        update_html_chapter(ch)
    
    print("\n" + "=" * 60)
    print("Updating Database Files (db.json, seed.json, db.backup.json)")
    print("=" * 60)
    update_database_files()
    print("\nAll updates completed successfully!")

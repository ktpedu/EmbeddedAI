import os
import re
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

CHAPTER_DATA = {
    1: {
        'yt': 'https://www.youtube.com/watch?v=oVg57hOrU4s',
        'pdf': 'https://app.box.com/s/vvstsd7x58cf4eoj9s03ftglpgd3d434',
        'pdf_title': 'เอกสารประกอบการบรรยาย (Box: Arduino App Lab & Board Setup)',
        'episodes': [
            {"ep": "Ep.01", "title": "การติดตั้ง Arduino App Lab บนคอมพิวเตอร์", "video_url": "https://www.youtube.com/watch?v=oVg57hOrU4s"},
            {"ep": "Ep.02", "title": "การติดตั้งและตรวจสอบ Debian Linux OS บน UNO Q", "video_url": "https://www.youtube.com/watch?v=IUrO0bfUvc0"},
            {"ep": "Ep.03", "title": "การตั้งค่าเริ่มต้นบอร์ด Arduino UNO Q เพื่อใช้ App Lab", "video_url": "https://www.youtube.com/watch?v=cRO5jjGtE_k"},
            {"ep": "Ep.04", "title": "เริ่มต้นสร้างแอปพลิเคชันใช้งานร่วมกับ Arduino UNO Q", "video_url": "https://www.youtube.com/watch?v=nO3FicIusQs"},
            {"ep": "Ep.29", "title": "เริ่มต้นใช้งาน Edge Impulse เพื่อเทรนโมเดล AI", "video_url": "https://www.youtube.com/watch?v=-X8y_aeMAFY&t=52s"}
        ]
    },
    2: {
        'yt': 'https://www.youtube.com/watch?v=g4sF5nnsSeY',
        'pdf': 'https://app.box.com/s/vvstsd7x58cf4eoj9s03ftglpgd3d434',
        'pdf_title': 'เอกสารประกอบการบรรยาย (Box: Arduino App Lab & Modular Brick)',
        'episodes': [
            {"ep": "Ep.05", "title": "การทำงานของวงรอบประมวลผล App.run()", "video_url": "https://www.youtube.com/watch?v=g4sF5nnsSeY"},
            {"ep": "Ep.06", "title": "การโปรแกรมบอร์ด Single-Board Mode & Desktop Linux", "video_url": "https://www.youtube.com/watch?v=DVCrb6t5dls"},
            {"ep": "Ep.07", "title": "การโปรแกรมบอร์ดในโหมดเครือข่ายไร้สาย (Network Mode)", "video_url": "https://www.youtube.com/watch?v=zu6CBc-GZpM"},
            {"ep": "Ep.08", "title": "เริ่มต้นสร้าง App เพื่อใช้งานแสดงข้อความบนคอนโซล", "video_url": "https://www.youtube.com/watch?v=pcw_iF02Ros"},
            {"ep": "Ep.09", "title": "สร้าง App เพื่อใช้ควบคุมบอร์ด LED บนบอร์ด Arduino UNO Q ตอนที่ 1", "video_url": "https://www.youtube.com/watch?v=7JBtwM5m-YI"},
            {"ep": "Ep.10", "title": "สร้าง App เพื่อใช้ควบคุมบอร์ด LED บนบอร์ด Arduino UNO Q ตอนที่ 2", "video_url": "https://www.youtube.com/watch?v=36Z_RYn6pQI"},
            {"ep": "Ep.05–12", "title": "Modular Brick & Hardware I/O (Playlist)", "video_url": "https://youtube.com/playlist?list=PL_P41WM_1HxGmyUuNPQQsDa-ItaDu5VyU"}
        ]
    },
    3: {
        'yt': 'https://www.youtube.com/watch?v=N-tZirbAWCE',
        'pdf': 'https://app.box.com/s/jk0x5i37qc670f0kmwuisougd3kj8j4p',
        'pdf_title': 'เอกสารประกอบการบรรยาย (Box: Database-SQL & Time Series Brick)',
        'episodes': [
            {"ep": "Ep.16", "title": "รู้จักกับ \"Database-SQL Brick\" บน Arduino App Lab", "video_url": "https://www.youtube.com/watch?v=N-tZirbAWCE"},
            {"ep": "Ep.17", "title": "รู้จักกับ \"Database-Time Series Brick\" บน Arduino App Lab", "video_url": "https://www.youtube.com/watch?v=MekwqhTuTzc"}
        ]
    },
    4: {
        'yt': 'https://www.youtube.com/watch?v=-X8y_aeMAFY&t=52s',
        'pdf': 'https://app.box.com/s/3gl7jnelf5uj39csjocopzsphuc8i0pu',
        'pdf_title': 'เอกสารประกอบการบรรยาย (Box: Edge Impulse Studio & Data Pipeline)',
        'episodes': [
            {"ep": "Ep.29", "title": "เริ่มต้นใช้งาน Edge Impulse เพื่อเทรนโมเดล AI", "video_url": "https://www.youtube.com/watch?v=-X8y_aeMAFY&t=52s"}
        ]
    },
    5: {
        'yt': 'https://www.youtube.com/watch?v=1yEMEJnsrUY',
        'pdf': 'https://app.box.com/s/3gl7jnelf5uj39csjocopzsphuc8i0pu',
        'pdf_title': 'เอกสารประกอบการบรรยาย (Box: Visual Anomaly Detection FOMO-AD)',
        'episodes': [
            {"ep": "Ep.30", "title": "การฝึกสอนโมเดล Visual Anomaly Detection (FOMO-AD)", "video_url": "https://www.youtube.com/watch?v=1yEMEJnsrUY"}
        ]
    },
    6: {
        'yt': 'https://www.youtube.com/watch?v=3mAwLsQjv6U',
        'pdf': 'https://app.box.com/s/3gl7jnelf5uj39csjocopzsphuc8i0pu',
        'pdf_title': 'เอกสารประกอบการบรรยาย (Box: Deploy .eim & app.yaml Configuration)',
        'episodes': [
            {"ep": "Ep.33", "title": "การนำโมเดล (.eim) สู่บอร์ด Arduino UNO Q", "video_url": "https://www.youtube.com/watch?v=3mAwLsQjv6U"},
            {"ep": "Ep.35", "title": "ถ่ายซ่อมการแก้ไขไฟล์ app.yaml", "video_url": "https://www.youtube.com/watch?v=0g2F-s-7O2U"}
        ]
    },
    7: {
        'yt': 'https://www.youtube.com/watch?v=5Xiz_W53yU0',
        'pdf': 'https://app.box.com/s/5fc91neqpantexqez8yr9vjfv9fc5s6b',
        'pdf_title': 'เอกสารประกอบการบรรยาย (Box: VAD Brick & Database-SQL Logging)',
        'episodes': [
            {"ep": "Ep.34", "title": "รู้จักกับ Visual Anomaly Detection Brick บน Arduino App Lab", "video_url": "https://www.youtube.com/watch?v=5Xiz_W53yU0"}
        ]
    },
    8: {
        'yt': 'https://www.youtube.com/watch?v=glQx9GTLEUI',
        'pdf': 'https://app.box.com/s/13lyv179wa2fo0igkep1i977e13dv6kd',
        'pdf_title': 'เอกสารประกอบการบรรยาย (Box: FOMO Object Detection Architecture)',
        'episodes': [
            {"ep": "Ep.31", "title": "การฝึกสอนโมเดล AI ให้ใช้กับงาน Object Detection (FOMO)", "video_url": "https://www.youtube.com/watch?v=glQx9GTLEUI"},
            {"ep": "Ep.18", "title": "รู้จักกับ Object Detection Brick บน Arduino App Lab", "video_url": "https://www.youtube.com/watch?v=mkmYqMgfaUw"}
        ]
    },
    9: {
        'yt': 'https://www.youtube.com/watch?v=6DlVYQzgrEw',
        'pdf': 'https://app.box.com/s/13lyv179wa2fo0igkep1i977e13dv6kd',
        'pdf_title': 'เอกสารประกอบการบรรยาย (Box: FOMO Centroid Tracking & Actuator Control)',
        'episodes': [
            {"ep": "Ep.42", "title": "Object Detection ผ่านกล้องเว็บแคม และคุม Actuator", "video_url": "https://www.youtube.com/watch?v=6DlVYQzgrEw"},
            {"ep": "Ep.31", "title": "การฝึกสอนโมเดล Object Detection (FOMO)", "video_url": "https://www.youtube.com/watch?v=glQx9GTLEUI"}
        ]
    },
    10: {
        'yt': 'https://www.youtube.com/watch?v=3EmkC1QBZK0',
        'pdf': 'https://app.box.com/s/3gl7jnelf5uj39csjocopzsphuc8i0pu',
        'pdf_title': 'เอกสารประกอบการบรรยาย (Box: Image Classification Transfer Learning)',
        'episodes': [
            {"ep": "Ep.32", "title": "การฝึกสอนโมเดล Image Classification (Brick)", "video_url": "https://www.youtube.com/watch?v=3EmkC1QBZK0"},
            {"ep": "Ep.43", "title": "Image Classification ผ่านกล้องเว็บแคม", "video_url": "https://www.youtube.com/watch?v=bLw9BH5RrFo"},
            {"ep": "Ep.22", "title": "รู้จักกับ Image Classification Brick บน Arduino App Lab", "video_url": "https://www.youtube.com/watch?v=Hwm797kDhbE"}
        ]
    },
    11: {
        'yt': 'https://www.youtube.com/watch?v=CRpBHlDRh60',
        'pdf': 'https://app.box.com/s/hh6m3noroe5dz932y7f6e0hklb6iuj21',
        'pdf_title': 'เอกสารประกอบการบรรยาย (Box: Keyword Spotting KWS MFCC Audio)',
        'episodes': [
            {"ep": "Ep.44", "title": "Keyword Spotting ผ่านไมโครโฟน (คำสั่งไทย)", "video_url": "https://www.youtube.com/watch?v=CRpBHlDRh60"},
            {"ep": "Ep.36", "title": "การฝึกสอนโมเดล Keyword Spotting (Brick)", "video_url": "https://www.youtube.com/watch?v=Lt5RQeWXZBA"},
            {"ep": "Ep.37", "title": "รู้จักกับ Keyword Spotting Brick ตอนที่ 1/2", "video_url": "https://www.youtube.com/watch?v=Ty9b9Zs9h-o"}
        ]
    },
    12: {
        'yt': 'https://www.youtube.com/watch?v=OSzculUyvaY',
        'pdf': 'https://app.box.com/s/m1zd2ahqm8xb20ozfig7h4gow6rhjmi1',
        'pdf_title': 'เอกสารประกอบการบรรยาย (Box: Audio Classification Acoustic AI)',
        'episodes': [
            {"ep": "Ep.45", "title": "Audio Classification ผ่านไมโครโฟน", "video_url": "https://www.youtube.com/watch?v=OSzculUyvaY"},
            {"ep": "Ep.39", "title": "การฝึกสอนโมเดล Audio Classification (Brick)", "video_url": "https://www.youtube.com/watch?v=9R-vpS6F4jA"},
            {"ep": "Ep.40", "title": "รู้จักกับ Audio Classification Brick ตอนที่ 1/2", "video_url": "https://www.youtube.com/watch?v=6xLtYZOkvfA"}
        ]
    }
}

# 1. Update HTML hero action buttons
print("=== UPDATING CHAPTER HTML FILES ===")
for ch, info in CHAPTER_DATA.items():
    ch_str = f"{ch:02d}"
    fpath = f"web_learning_platform/public/chapter{ch_str}.html"
    if not os.path.exists(fpath):
        print(f"File not found: {fpath}")
        continue
    
    with open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 1.1 Replace YouTube link in Hero
    # Look for: <a href="[^"]+" target="_blank" class="bg-white/10 hover:bg-white/20 text-white border border-white/30 px-5 py-2.5 rounded-xl text-xs sm:text-sm font-bold flex items-center gap-2 transition"[^>]*>\s*<i class="fa-brands fa-youtube text-red-400 text-base"></i> สื่อวีดิทัศน์ประจำบทเรียน\s*</a>
    pattern_yt = r'<a href="[^"]+" target="_blank" class="bg-white/10 hover:bg-white/20 text-white border border-white/30 px-5 py-2.5 rounded-xl text-xs sm:text-sm font-bold flex items-center gap-2 transition"[^>]*>\s*<i class="fa-brands fa-youtube text-red-400 text-base"></i> สื่อวีดิทัศน์ประจำบทเรียน\s*</a>'
    new_yt = f'<a href="{info["yt"]}" target="_blank" class="bg-white/10 hover:bg-white/20 text-white border border-white/30 px-5 py-2.5 rounded-xl text-xs sm:text-sm font-bold flex items-center gap-2 transition" title="สื่อวีดิทัศน์ประจำบทเรียน">\n            <i class="fa-brands fa-youtube text-red-400 text-base"></i> สื่อวีดิทัศน์ประจำบทเรียน\n          </a>'
    
    html_new, count_yt = re.subn(pattern_yt, new_yt, html)
    
    # 1.2 Replace PDF link in Hero
    pattern_pdf = r'<a href="https?://(?:app\.)?box\.com/s/[a-zA-Z0-9_-]+" target="_blank"[^>]*>\s*<i class="fa-solid fa-file-pdf"></i>\s*เอกสารประกอบการบรรยาย \(PDF\)\s*</a>'
    new_pdf = f'<a href="{info["pdf"]}" target="_blank" rel="noopener noreferrer" class="bg-blue-600/70 hover:bg-blue-600 text-white px-4 py-2.5 rounded-xl text-xs sm:text-sm font-bold flex items-center gap-2 transition" title="{info["pdf_title"]}">\n            <i class="fa-solid fa-file-pdf"></i> เอกสารประกอบการบรรยาย (PDF)\n          </a>'
    
    html_new, count_pdf = re.subn(pattern_pdf, new_pdf, html_new)
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html_new)
        
    print(f"Chapter {ch_str}: Updated YT ({count_yt} matches), PDF ({count_pdf} matches)")

# 2. Update Database JSON files
print("\n=== UPDATING DB / SEED / BACKUP JSON FILES ===")
db_files = [
    'web_learning_platform/data/db.json',
    'web_learning_platform/data/seed.json',
    'web_learning_platform/data/db.backup.json'
]

for db_path in db_files:
    if not os.path.exists(db_path):
        continue
    with open(db_path, 'r', encoding='utf-8') as f:
        db = json.load(f)
        
    for lesson in db.get('lessons', []):
        ch_num = lesson.get('chapter_number')
        if ch_num in CHAPTER_DATA:
            info = CHAPTER_DATA[ch_num]
            lesson['video_url'] = info['yt']
            lesson['slide_url'] = info['pdf']
            lesson['pdf_url'] = info['pdf']
            lesson['video_episodes'] = info['episodes']
            
    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    print(f"Successfully updated all 12 lessons in {db_path}")

print("\nDone! All files synchronized.")

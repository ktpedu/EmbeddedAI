import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, 'web_learning_platform', 'data')

CH01_EPISODES = [
    {
        "ep": "Ep.01",
        "title": "การติดตั้งโปรแกรมสภาพแวดล้อม Arduino App Lab บนคอมพิวเตอร์",
        "video_url": "https://www.youtube.com/watch?v=oVg57hOrU4s"
    },
    {
        "ep": "Ep.02",
        "title": "การติดตั้งและตรวจสอบระบบปฏิบัติการ Debian Linux บนบอร์ดพัฒนา Arduino UNO Q",
        "video_url": "https://www.youtube.com/watch?v=IUrO0bfUvc0"
    },
    {
        "ep": "Ep.03",
        "title": "การตั้งค่าเริ่มต้นบอร์ด Arduino UNO Q เพื่อใช้งานร่วมกับ Arduino App Lab",
        "video_url": "https://www.youtube.com/watch?v=cRO5jjGtE_k"
    },
    {
        "ep": "Ep.04",
        "title": "เริ่มต้นสร้างแอปพลิเคชันและการควบคุมบอร์ดพัฒนาด้วย Arduino App Lab",
        "video_url": "https://www.youtube.com/watch?v=nO3FicIusQs"
    },
    {
        "ep": "Ep.29",
        "title": "เริ่มต้นใช้งาน Edge Impulse เพื่อเทรนโมเดล AI",
        "video_url": "https://www.youtube.com/watch?v=-X8y_aeMAFY&t=52s"
    }
]

for filename in ['db.json', 'seed.json', 'db.backup.json']:
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    lessons = data.get('lessons', [])
    for l in lessons:
        if l.get('id') == 'ch01' or l.get('chapter_number') == 1:
            l['video_episodes'] = CH01_EPISODES
            # Default video_url can be Ep.01 or Ep.29
            l['video_url'] = 'https://www.youtube.com/watch?v=oVg57hOrU4s'
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"[OK] Enriched Chapter 1 video_episodes in {filename}")

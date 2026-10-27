import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

BOX_CH01_URL = "https://app.box.com/s/vvstsd7x58cf4eoj9s03ftglpgd3d434"

files = [
    'web_learning_platform/data/db.json',
    'web_learning_platform/data/seed.json',
    'web_learning_platform/data/db.backup.json'
]

for filepath in files:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 1. Update lessons ch01
        for lesson in data.get('lessons', []):
            if lesson.get('id') == 'ch01':
                lesson['slide_url'] = BOX_CH01_URL
                lesson['pdf_url'] = BOX_CH01_URL
                print(f"Updated lesson ch01 in {filepath}")
        
        # 2. Update materials mat_01
        for mat in data.get('materials', []):
            if mat.get('chapter_id') == 'ch01' or mat.get('id') == 'mat_01':
                mat['url'] = BOX_CH01_URL
                mat['title'] = 'เอกสารประกอบการบรรยาย: Arduino App Lab (Box คลังเอกสารบทที่ 1)'
                print(f"Updated material mat_01 in {filepath}")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Successfully saved {filepath}")
    except Exception as e:
        print(f"Error updating {filepath}: {e}")

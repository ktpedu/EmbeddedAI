import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

BOX_CH07_URL = "https://app.box.com/s/5fc91neqpantexqez8yr9vjfv9fc5s6b"

files = [
    'web_learning_platform/data/db.json',
    'web_learning_platform/data/seed.json',
    'web_learning_platform/data/db.backup.json'
]

for filepath in files:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for lesson in data.get('lessons', []):
            if lesson.get('id') == 'ch07':
                lesson['slide_url'] = BOX_CH07_URL
                lesson['pdf_url'] = BOX_CH07_URL
                print(f"Updated lesson ch07 in {filepath}")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error {filepath}: {e}")

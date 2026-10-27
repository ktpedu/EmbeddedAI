import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('web_learning_platform/data/db.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

for l in db['lessons']:
    if l['id'] == 'ch02':
        print(json.dumps(l, ensure_ascii=False, indent=2))

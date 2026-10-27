import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('web_learning_platform/data/db.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

for l in db.get('lessons', []):
    print(f"{l.get('id')}: duration={l.get('duration')}, title={l.get('title')}")

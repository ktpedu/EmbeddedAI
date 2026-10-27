import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('web_learning_platform/public/index.html', 'r', encoding='utf-8') as f:
    idx = f.read()

pos = idx.find('section-lessons')
print("Position:", pos)
section_chunk = idx[pos:pos+15000]

# find all chapter references
for m in re.finditer(r'(chapter\d+\.html)', section_chunk):
    # print surrounding context
    st = max(0, m.start() - 100)
    en = min(len(section_chunk), m.end() + 200)
    print("---", m.group(1), "---")
    print(section_chunk[st:en])
    print()

import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

for c in range(2, 13):
    filename = f"web_learning_platform/public/chapter{c:02d}.html"
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()
    
    missing = []
    if "รายการครุภัณฑ์และอุปกรณ์ปฏิบัติการ" not in html:
        missing.append("Equipment Card")
    if "ข้อมูลจำเพาะประจำบทเรียน" not in html:
        missing.append("Hero Meta Card")
    if "คำถามทบทวนองค์ความรู้" not in html and "คำถามประเมินความเข้าใจ" not in html:
        missing.append("Review Questions")
    if "ภารกิจปฏิบัติการ" not in html and "การประเมินสมรรถนะ" not in html:
        missing.append("Checklist")
    if "แบบทดสอบท้ายบทเรียน" not in html:
        missing.append("Quiz Callout Card")
    if "learning-enhancements.js" not in html:
        missing.append("Enhancements JS")
    
    print(f"Chapter {c:02d}: Missing -> {missing if missing else 'None (Fully Standardized)'}")

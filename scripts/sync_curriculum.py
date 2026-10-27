#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
เครื่องมือตรวจสอบและซิงโครไนซ์ข้อมูลหลักสูตร (Curriculum Synchronization Utility)
รายวิชา: ปัญญาประดิษฐ์บนระบบสมองกลฝังตัว (Embedded Artificial Intelligence)
--------------------------------------------------------------------------------
ฟังก์ชันการทำงาน:
1. ตรวจสอบความสอดคล้องระหว่างฐานข้อมูลเว็บบทเรียน (db.json) และเอกสาร Markdown
2. รายงานสรุปสถานะความสมบูรณ์ของบทเรียน ข้อสอบ และใบงาน
================================================================================
"""

import os
import sys
import json
import re

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT_DIR, 'web_learning_platform', 'data', 'db.json')
LESSON_MD = os.path.join(ROOT_DIR, 'เนื้อหาบทเรียนละเอียด_EdgeAI.md')
WORKSHEET_MD = os.path.join(ROOT_DIR, 'ใบงานปฏิบัติการ_EdgeAI.md')
QUIZ_MD = os.path.join(ROOT_DIR, 'ข้อสอบปรนัย_แยกรายบท_120ข้อ.md')

def check_sync():
    print("=" * 65)
    print(" รายงานการตรวจสอบความสอดคล้องข้อมูลหลักสูตร (Curriculum Audit)")
    print("=" * 65)

    if not os.path.exists(DB_PATH):
        print(f"[!] ไม่พบไฟล์ฐานข้อมูล: {DB_PATH}")
        return False

    with open(DB_PATH, 'r', encoding='utf-8') as f:
        db = json.load(f)

    lessons = db.get('lessons', [])
    quizzes = db.get('quizzes', [])
    practicals = db.get('practical_exams', [])
    worksheets = db.get('worksheets', [])
    materials = db.get('materials', [])

    print(f"[*] จำนวนบทเรียนในฐานข้อมูล (db.json) : {len(lessons)} บท")
    print(f"[*] จำนวนข้อสอบในคลัง (Quizzes)       : {len(quizzes)} ข้อ")
    print(f"[*] จำนวนโจทย์ปฏิบัติ (Practicals)     : {len(practicals)} ภารกิจ")
    print(f"[*] จำนวนใบงานห้องทดลอง (Worksheets) : {len(worksheets)} ใบงาน")
    print(f"[*] จำนวนสื่อประกอบ (Materials)        : {len(materials)} รายการ")
    print("-" * 65)

    # Check Markdown Document Integrity
    for md_path, name in [(LESSON_MD, "เอกสารเนื้อหาบทเรียน"), (WORKSHEET_MD, "เอกสารใบงาน"), (QUIZ_MD, "เอกสารคลังข้อสอบ")]:
        if os.path.exists(md_path):
            size_kb = round(os.path.getsize(md_path) / 1024, 1)
            print(f"[OK] {name:<22} : พบไฟล์ ({size_kb} KB) -> {os.path.basename(md_path)}")
        else:
            print(f"[!] {name:<22} : ไม่พบไฟล์ -> {os.path.basename(md_path)}")

    # Check Forbidden / Deprecated Terms
    print("-" * 65)
    print("[*] สแกนตรวจคำต้องห้ามในฐานข้อมูล db.json:")
    forbidden = [r'ม\.5', r'มัธยมศึกษาปีที่\s*5', r'\(Ep\.16\)', r'ปพ\.5']
    found_issues = 0
    raw_db = json.dumps(db, ensure_ascii=False)
    for p in forbidden:
        m = re.findall(p, raw_db)
        if m:
            print(f"  [!] พบคำต้องห้าม '{p}': {len(m)} รายการ")
            found_issues += 1

    if found_issues == 0:
        print("  [OK] ผ่านการตรวจสอบ 100%! ไม่พบคำต้องห้ามหลงเหลือในฐานข้อมูล")

    print("=" * 65)
    return True

if __name__ == '__main__':
    check_sync()

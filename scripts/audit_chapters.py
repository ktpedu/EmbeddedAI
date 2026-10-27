import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

chapters = range(1, 13)
for c in chapters:
    filename = f"web_learning_platform/public/chapter{c:02d}.html"
    if not os.path.exists(filename):
        print(f"MISSING: {filename}")
        continue
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()
    
    has_top_bar = "KT-Edu Learning Module" in html
    has_depa_header = "MAIN HEADER (depa THEME)" in html
    has_progress_strip = f"บทเรียนที่ {c}" in html
    has_3_actions = "เริ่มต้นศึกษาเนื้อหา" in html and "สื่อวีดิทัศน์ประจำบทเรียน" in html and "เอกสารประกอบการบรรยาย" in html
    has_meta_card = "ข้อมูลจำเพาะประจำบทเรียน" in html
    has_enhancements_js = "learning-enhancements.js" in html
    has_pager = "สารบัญบทเรียน" in html
    has_rubric = "การประเมินสมรรถนะการปฏิบัติการ" in html or "เกณฑ์การประเมิน" in html
    has_review = "คำถามทบทวนองค์ความรู้" in html
    
    # Check for any lingering inline video buttons in section headers
    has_inline_video = "openVideoByEpisode" in html
    
    # Check PDF link
    pdf_m = re.search(r'href="(https://app\.box\.com/[^"]+)"[^>]*>[^<]*<i class="fa-solid fa-file-pdf"', html)
    pdf_link = pdf_m.group(1) if pdf_m else "NOT FOUND"
    
    # Check Video link in Hero
    vid_m = re.search(r'href="(https://(?:www\.)?youtube\.com/[^"]+)"[^>]*>[^<]*<i class="fa-brands fa-youtube[^"]*"></i>\s*สื่อวีดิทัศน์ประจำบทเรียน', html)
    hero_vid = vid_m.group(1) if vid_m else "NOT FOUND"

    print(f"=== Chapter {c:02d} ===")
    print(f"  TopBar: {has_top_bar} | DepaHeader: {has_depa_header} | Strip: {has_progress_strip} | 3Actions: {has_3_actions} | MetaCard: {has_meta_card}")
    print(f"  EnhancementsJS: {has_enhancements_js} | Pager: {has_pager} | Rubric: {has_rubric} | Review: {has_review}")
    print(f"  InlineVideoButtons: {has_inline_video}")
    print(f"  PDF Link: {pdf_link}")
    print(f"  Hero Video: {hero_vid}")

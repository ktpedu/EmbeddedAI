import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

for ch in range(1, 13):
    ch_str = f"{ch:02d}"
    fpath = f"web_learning_platform/public/chapter{ch_str}.html"
    if not os.path.exists(fpath):
        continue
    with open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Find Hero action buttons
    m_yt = re.search(r'<a href="([^"]+)"[^>]*>\s*<i class="fa-brands fa-youtube[^"]*"></i>\s*สื่อวีดิทัศน์ประจำบทเรียน', html)
    m_pdf = re.search(r'<a href="([^"]+)"[^>]*>\s*<i class="fa-solid fa-file-pdf"></i>\s*เอกสารประกอบการบรรยาย \(PDF\)', html)
    
    yt_url = m_yt.group(1) if m_yt else 'NOT FOUND'
    pdf_url = m_pdf.group(1) if m_pdf else 'NOT FOUND'
    
    print(f"Chapter {ch_str}:")
    print(f"   YT : {yt_url}")
    print(f"   PDF: {pdf_url}")

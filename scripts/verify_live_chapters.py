import urllib.request
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== VERIFYING ALL LIVE CHAPTER PAGES ===")
for ch in range(1, 13):
    ch_str = f"{ch:02d}"
    url = f"http://localhost:3001/chapter{ch_str}.html"
    try:
        resp = urllib.request.urlopen(url)
        html = resp.read().decode('utf-8')
        m_yt = re.search(r'<a href="([^"]+)"[^>]*>\s*<i class="fa-brands fa-youtube[^"]*"></i>\s*สื่อวีดิทัศน์ประจำบทเรียน', html)
        m_pdf = re.search(r'<a href="([^"]+)"[^>]*>\s*<i class="fa-solid fa-file-pdf"></i>\s*เอกสารประกอบการบรรยาย \(PDF\)', html)
        
        yt = m_yt.group(1) if m_yt else 'NONE'
        pdf = m_pdf.group(1) if m_pdf else 'NONE'
        print(f"Chapter {ch_str} ({resp.status}): YT={yt} | PDF={pdf}")
    except Exception as e:
        print(f"Chapter {ch_str}: ERROR {e}")

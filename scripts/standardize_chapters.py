import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

CHAPTER_META = {
    2: {
        "title": "สถาปัตยกรรมซอฟต์แวร์แบบมอดูล (Modular Brick) และการควบคุมฮาร์ดแวร์พื้นฐาน",
        "time": "3 คาบ (150 นาที)",
        "target_arch": "Arduino UNO Q (IPC Bus)",
        "software": "Modular Brick & LED Matrix",
        "code_folder": "chapter02",
        "pdf_url": "https://app.box.com/s/3gl7jnelf5uj39csjocopzsphuc8i0pu",
        "equipment": [
            "บอร์ดพัฒนา Arduino UNO Q (ชิปหน่วยประมวลผล Qualcomm Dragonwing QRB2210)",
            "สายเชื่อมต่อ USB Type-C (ชนิดรับส่งข้อมูลและจ่ายกำลังไฟฟ้า 3A)",
            "หน้าจอ LED Matrix ขนาด 8x13 พิกเซล และสวิตช์ปุ่มกด User Button บนตัวบอร์ด",
            "เครื่องคอมพิวเตอร์พร้อมโปรแกรมสภาพแวดล้อม Arduino App Lab"
        ]
    },
    3: {
        "title": "การจัดการระบบฐานข้อมูลบนอุปกรณ์ด้วย Database-SQL Brick",
        "time": "3 คาบ (150 นาที)",
        "target_arch": "Arduino UNO Q (SQLite 3)",
        "software": "Database-SQL Brick & Python",
        "code_folder": "chapter03",
        "pdf_url": "https://app.box.com/s/3gl7jnelf5uj39csjocopzsphuc8i0pu",
        "equipment": [
            "บอร์ดพัฒนา Arduino UNO Q (ชิปหน่วยประมวลผล Qualcomm Dragonwing QRB2210)",
            "สายเชื่อมต่อ USB Type-C (ชนิดรับส่งข้อมูลและจ่ายกำลังไฟฟ้า 3A)",
            "ระบบหน่วยความจำ Flash Storage 16GB สำหรับจัดเก็บฐานข้อมูล SQLite 3",
            "เครื่องคอมพิวเตอร์พร้อมโปรแกรมสภาพแวดล้อม Arduino App Lab และ SQLite Viewer"
        ]
    },
    4: {
        "title": "การจัดเตรียมชุดข้อมูลและการออกแบบขั้นตอนการประมวลผล (Data Pipeline) บน Edge Impulse",
        "time": "3 คาบ (150 นาที)",
        "target_arch": "Edge Impulse Studio (Cloud/Local)",
        "software": "Data Acquisition & Impulse Design",
        "code_folder": "chapter04",
        "pdf_url": "https://app.box.com/s/3gl7jnelf5uj39csjocopzsphuc8i0pu",
        "equipment": [
            "บอร์ดพัฒนา Arduino UNO Q (ชิปหน่วยประมวลผล Qualcomm Dragonwing QRB2210)",
            "กล้อง USB UVC Webcam สำหรับการบันทึกภาพตัวอย่างเข้าสู่ Data Acquisition",
            "บัญชีผู้ใช้งานแพลตฟอร์ม Edge Impulse Studio สำหรับจัดการ Data Pipeline",
            "สายเชื่อมต่อ USB Type-C และโครงข่ายสัญญาณอินเทอร์เน็ต"
        ]
    },
    5: {
        "title": "การฝึกสอนโมเดลตรวจจับความผิดปกติจากภาพ (Visual Anomaly Detection)",
        "time": "4 คาบ (200 นาที)",
        "target_arch": "FOMO-AD (AArch64 MobileNetV2)",
        "software": "Visual Anomaly Brick & Studio",
        "code_folder": "chapter05",
        "pdf_url": "https://app.box.com/s/3gl7jnelf5uj39csjocopzsphuc8i0pu",
        "equipment": [
            "บอร์ดพัฒนา Arduino UNO Q (ชิปหน่วยประมวลผล Qualcomm Dragonwing QRB2210)",
            "กล้อง USB UVC Webcam พร้อมขาตั้งสำหรับจับภาพชิ้นงานในสายการผลิตจำลอง",
            "ชิ้นงานตัวอย่างสำหรับฝึกสอน (ชิ้นงานปกติ 100+ ตัวอย่าง) และชิ้นงานทดสอบความผิดปกติ",
            "สายเชื่อมต่อ USB Type-C และโปรแกรม Arduino App Lab"
        ]
    },
    6: {
        "title": "การนำโมเดล .eim ไปใช้งานและการกำหนดค่าไฟล์ app.yaml บนบอร์ดพัฒนา Arduino UNO Q",
        "time": "3 คาบ (150 นาที)",
        "target_arch": "Debian Linux AArch64 (.eim Binary)",
        "software": "app.yaml & Terminal SSH/Console",
        "code_folder": "chapter06",
        "pdf_url": "https://app.box.com/s/3gl7jnelf5uj39csjocopzsphuc8i0pu",
        "equipment": [
            "บอร์ดพัฒนา Arduino UNO Q พร้อมระบบปฏิบัติการ Debian Linux 12 AArch64",
            "ไฟล์ไบนารีโมเดลปัญญาประดิษฐ์ .eim ที่ผ่านการคอมไพล์สำหรับ Linux AArch64",
            "โปรแกรมสภาพแวดล้อม Arduino App Lab และระบบคอนโซลคำสั่ง Terminal (SSH)",
            "สายเชื่อมต่อ USB Type-C และระบบเครือข่าย Wi-Fi/LAN"
        ]
    },
    7: {
        "title": "การประมวลผลโมเดลตรวจจับความผิดปกติจากภาพ และการบันทึกข้อมูลลง Database-SQL Brick",
        "time": "3 คาบ (150 นาที)",
        "target_arch": "Arduino UNO Q (VAD + SQLite)",
        "software": "VAD Brick & Database-SQL Brick",
        "code_folder": "chapter07",
        "pdf_url": "https://app.box.com/s/5fc91neqpantexqez8yr9vjfv9fc5s6b",
        "equipment": [
            "บอร์ดพัฒนา Arduino UNO Q (ชิปหน่วยประมวลผล Qualcomm Dragonwing QRB2210)",
            "กล้อง USB UVC Webcam สำหรับการตรวจจับภาพชิ้นงานแบบเรียลไทม์",
            "โมเดล VAD .eim และมอดูล Database-SQL Brick สำหรับบันทึก Event Log",
            "สายเชื่อมต่อ USB Type-C และโปรแกรม Arduino App Lab"
        ]
    },
    8: {
        "title": "การฝึกสอนโมเดลตรวจจับวัตถุด้วยสถาปัตยกรรม FOMO (Object Detection)",
        "time": "4 คาบ (200 นาที)",
        "target_arch": "FOMO Object Detection (0.35/0.1)",
        "software": "FOMO Brick & Edge Impulse Studio",
        "code_folder": "chapter08",
        "pdf_url": "https://app.box.com/s/3gl7jnelf5uj39csjocopzsphuc8i0pu",
        "equipment": [
            "บอร์ดพัฒนา Arduino UNO Q (ชิปหน่วยประมวลผล Qualcomm Dragonwing QRB2210)",
            "กล้อง USB UVC Webcam พร้อมฉากและแท่นวางวัตถุสำหรับกำหนด Bounding Box",
            "วัตถุหรือชิ้นส่วนเป้าหมายสำหรับการตรวจจับตำแหน่งจุดกึ่งกลาง (Centroid)",
            "สายเชื่อมต่อ USB Type-C และบัญชี Edge Impulse Studio"
        ]
    },
    9: {
        "title": "การนำโมเดล FOMO ไปใช้งานและการควบคุมอุปกรณ์ขับเคลื่อน (Actuator)",
        "time": "4 คาบ (200 นาที)",
        "target_arch": "Arduino UNO Q + Actuators",
        "software": "FOMO .eim & Servo Control App",
        "code_folder": "chapter09",
        "pdf_url": "https://app.box.com/s/3gl7jnelf5uj39csjocopzsphuc8i0pu",
        "equipment": [
            "บอร์ดพัฒนา Arduino UNO Q (ชิปหน่วยประมวลผล Qualcomm Dragonwing QRB2210)",
            "กล้อง USB UVC Webcam สำหรับตรวจจับพิกัดวัตถุสด",
            "ชุดเซอร์โวมอเตอร์ (Servo Motor / Actuator) หรือโมดูลรีเลย์สำหรับคัดแยกชิ้นงาน",
            "สายเชื่อมต่อ USB Type-C, สายสัญญาณ Jumper Wires และแหล่งจ่ายไฟภายนอก 5V"
        ]
    },
    10: {
        "title": "การพัฒนาและประมวลผลโมเดลจำแนกประเภทภาพ (Image Classification)",
        "time": "3 คาบ (150 นาที)",
        "target_arch": "MobileNetV2 Transfer Learning",
        "software": "Image Classification Brick",
        "code_folder": "chapter10",
        "pdf_url": "https://app.box.com/s/3gl7jnelf5uj39csjocopzsphuc8i0pu",
        "equipment": [
            "บอร์ดพัฒนา Arduino UNO Q (ชิปหน่วยประมวลผล Qualcomm Dragonwing QRB2210)",
            "กล้อง USB UVC Webcam สำหรับการทดสอบ Inference สดผ่านหน้ากล้อง",
            "ชุดข้อมูลจำแนกประเภทภาพพร้อมคลาสฉากหลัง (Background / Unknown Class)",
            "สายเชื่อมต่อ USB Type-C และโปรแกรม Arduino App Lab"
        ]
    },
    11: {
        "title": "การประมวลผลสัญญาณเสียงและการฝึกสอนโมเดลรู้จำคำสั่งเสียง (Keyword Spotting: KWS)",
        "time": "3 คาบ (150 นาที)",
        "target_arch": "MFCC Feature + Neural Network",
        "software": "KWS Brick & Audio Pipeline",
        "code_folder": "chapter11",
        "pdf_url": "https://app.box.com/s/3gl7jnelf5uj39csjocopzsphuc8i0pu",
        "equipment": [
            "บอร์ดพัฒนา Arduino UNO Q (ชิปหน่วยประมวลผล Qualcomm Dragonwing QRB2210)",
            "โมดูลไมโครโฟน USB หรือโมดูลเสียงดิจิทัล I2S สำหรับรับสัญญาณเสียงคำสั่ง",
            "หลอดไฟ LED หรือตัวแสดงผลสถานะการรับคำสั่งเสียงภาษาไทย",
            "สายเชื่อมต่อ USB Type-C และโปรแกรม Arduino App Lab"
        ]
    },
    12: {
        "title": "การจำแนกเสียงเฉพาะทางและการบูรณาการระบบ Edge AI เชิงวิศวกรรม",
        "time": "4 คาบ (200 นาที)",
        "target_arch": "Multi-Modal Edge AI Integration",
        "software": "Audio Classification & Industrial Capstone",
        "code_folder": "chapter12",
        "pdf_url": "https://app.box.com/s/3gl7jnelf5uj39csjocopzsphuc8i0pu",
        "equipment": [
            "บอร์ดพัฒนา Arduino UNO Q (ชิปหน่วยประมวลผล Qualcomm Dragonwing QRB2210)",
            "ชุดเซนเซอร์พหุโมดอล (กล้อง USB UVC Webcam + ไมโครโฟนดิจิทัล)",
            "อุปกรณ์ขับเคลื่อนทางวิศวกรรม (Actuator / Relay / Emergency Interlock)",
            "ระบบจัดเก็บฐานข้อมูล SQLite สำหรับระบบบำรุงรักษาเชิงคาดการณ์ (Predictive Maintenance)"
        ]
    }
}

def make_equipment_card(c, meta):
    items_html = "\n".join([
        f'            <li class="flex items-start gap-2">\n'
        f'              <i class="fa-solid fa-check text-yellow-400 mt-0.5 text-[11px]"></i>\n'
        f'              <span>{item}</span>\n'
        f'            </li>'
        for item in meta["equipment"]
    ])
    
    return f'''        <!-- Card: Equipment & Target Board -->
        <div class="bg-gradient-to-br from-[#0d2342] to-[#173b6b] rounded-2xl p-4 sm:p-5 text-white shadow-md border border-white/10 space-y-3.5">
          <div class="text-xs font-bold text-yellow-300 uppercase tracking-wider flex items-center gap-1.5 border-b border-white/10 pb-2">
            <i class="fa-solid fa-microchip"></i> รายการครุภัณฑ์และอุปกรณ์ปฏิบัติการ
          </div>
          <ul class="text-xs space-y-2 text-slate-200">
{items_html}
          </ul>
        </div>

        <!-- Chapter Navigation Button -->
        <div class="bg-white rounded-2xl shadow-sm border border-slate-200 p-4 space-y-2">
          <a href="index.html?chapter={c}#section-quizzes" class="w-full btn-depa-yellow py-2.5 px-4 rounded-xl text-xs font-bold flex items-center justify-center gap-2 shadow">
            <i class="fa-solid fa-pen-to-square"></i> แบบทดสอบวัดผลสัมฤทธิ์บทที่ {c}
          </a>
          <a href="index.html?chapter={c}#section-worksheets" class="w-full bg-slate-100 hover:bg-slate-200 text-slate-800 py-2.5 px-4 rounded-xl text-xs font-bold flex items-center justify-center gap-2 transition">
            <i class="fa-solid fa-flask text-red-500"></i> ใบงานปฏิบัติการที่ {c}
          </a>
        </div>'''

def make_quiz_callout(c):
    return f'''        <!-- Quiz Callout Banner -->
        <div class="p-6 rounded-2xl bg-gradient-to-r from-blue-900 to-indigo-900 text-white shadow-lg border border-yellow-400/30 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div class="space-y-1 text-center sm:text-left">
            <div class="text-xs font-bold text-yellow-300 uppercase tracking-wider flex items-center justify-center sm:justify-start gap-1.5">
              <i class="fa-solid fa-graduation-cap"></i> แบบประเมินผลการเรียนรู้ประจำบทเรียน
            </div>
            <h4 class="text-lg font-black text-white">แบบทดสอบท้ายบทเรียนที่ {c} (ปรนัย 10 ข้อ)</h4>
            <p class="text-xs text-slate-200">ทดสอบความรู้ความเข้าใจตามเกณฑ์มาตรฐานตัวชี้วัดสาระเทคโนโลยี พร้อมเฉลยและบันทึกคะแนนอัตโนมัติ</p>
          </div>
          <a href="index.html?chapter={c}#section-quizzes" class="btn-depa-yellow px-6 py-3 rounded-xl text-xs sm:text-sm font-black shadow-xl flex items-center gap-2 shrink-0">
            <i class="fa-solid fa-pen-to-square"></i> เข้าทำแบบทดสอบ
          </a>
        </div>'''

for c in range(2, 13):
    filename = f"web_learning_platform/public/chapter{c:02d}.html"
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()
    
    meta = CHAPTER_META[c]
    modified = False

    # 1. Update PDF URL if needed (especially Chapter 7)
    if meta["pdf_url"] not in html:
        old_pdf_m = re.search(r'href="https://app\.box\.com/[^"]+"([^>]*><i class="fa-solid fa-file-pdf")', html)
        if old_pdf_m:
            html = re.sub(
                r'href="https://app\.box\.com/[^"]+"([^>]*><i class="fa-solid fa-file-pdf")',
                f'href="{meta["pdf_url"]}"\\1',
                html,
                count=1
            )
            modified = True
            print(f"Ch.{c:02d}: Updated PDF URL to {meta['pdf_url']}")

    # 2. Add Equipment Card to <aside> if missing
    if "รายการครุภัณฑ์และอุปกรณ์ปฏิบัติการ" not in html:
        # Find closing </aside> tag
        aside_end = html.find('</aside>')
        if aside_end != -1:
            equip_card = make_equipment_card(c, meta)
            html = html[:aside_end] + equip_card + "\n\n      " + html[aside_end:]
            modified = True
            print(f"Ch.{c:02d}: Added Equipment Card and Sidebar Action Buttons")

    # 3. Add Quiz Callout Banner before CHAPTER FOOTER & NAVIGATION PAGER if missing
    if "แบบทดสอบท้ายบทเรียนที่" not in html and "แบบทดสอบวัดผลสัมฤทธิ์บทที่" not in html[html.find('CHAPTER FOOTER'):]:
        pager_comment = html.find('<!-- CHAPTER FOOTER & NAVIGATION PAGER')
        if pager_comment != -1:
            quiz_banner = make_quiz_callout(c) + "\n\n        "
            html = html[:pager_comment] + quiz_banner + html[pager_comment:]
            modified = True
            print(f"Ch.{c:02d}: Added Quiz Callout Banner")

    # 4. Standardize Hero Meta Card in Chapters 9, 10, 11, 12 if needed
    if c in [9, 10, 11, 12] and "ข้อมูลจำเพาะประจำบทเรียน" not in html:
        # Replace the older meta card in Hero
        old_meta_pattern = r'<!-- Meta Card -->\s*<div class="bg-white/10[^>]*>.*?</div>\s*</div>\s*</div>\s*</section>'
        new_meta = f'''        <!-- Quick Lesson Meta Card -->
        <div class="bg-white/10 backdrop-blur-md rounded-2xl p-4 sm:p-5 border border-white/20 min-w-[280px] space-y-3 self-start lg:self-auto">
          <div class="text-xs text-yellow-300 font-bold uppercase tracking-wider flex items-center gap-1.5">
            <i class="fa-solid fa-circle-info"></i> ข้อมูลจำเพาะประจำบทเรียน
          </div>
          <div class="grid grid-cols-2 gap-3 text-xs">
            <div>
              <span class="text-slate-300 block text-[11px]">เวลาเรียน:</span>
              <span class="font-bold text-white text-sm">{meta["time"]}</span>
            </div>
            <div>
              <span class="text-slate-300 block text-[11px]">รูปแบบการเรียน:</span>
              <span class="font-bold text-yellow-300 text-sm">ทฤษฎี & ปฏิบัติการ</span>
            </div>
            <div>
              <span class="text-slate-300 block text-[11px]">สถาปัตยกรรมเป้าหมาย:</span>
              <span class="font-bold text-white">{meta["target_arch"]}</span>
            </div>
            <div>
              <span class="text-slate-300 block text-[11px]">ซอฟต์แวร์/มอดูลหลัก:</span>
              <span class="font-bold text-white">{meta["software"]}</span>
            </div>
          </div>
          <div class="pt-2 border-t border-white/10 flex items-center justify-between text-[11px]">
            <span class="text-slate-300"><i class="fa-solid fa-file-code mr-1"></i> โค้ดตัวอย่าง:</span>
            <a href="/code_examples/{meta['code_folder']}/" target="_blank" class="font-mono text-yellow-300 font-bold hover:text-white underline decoration-yellow-400 flex items-center gap-1.5" title="คลิกเพื่อเปิดโฟลเดอร์ไฟล์โค้ดของบทเรียนนี้">code_examples/{meta['code_folder']} <i class="fa-solid fa-arrow-up-right-from-square text-[10px]"></i></a>
          </div>
        </div>
      </div>
    </div>
  </section>'''
        if re.search(old_meta_pattern, html, re.DOTALL):
            html = re.sub(old_meta_pattern, new_meta, html, flags=re.DOTALL)
            modified = True
            print(f"Ch.{c:02d}: Standardized Hero Meta Card to match Chapter 1 layout")

    # 5. Ensure "สารบัญ" button exists in Chapter Navigation Pager
    pager_sec = re.search(r'(<!-- CHAPTER FOOTER & NAVIGATION PAGER.*?</div>\s*</div>)', html, re.DOTALL)
    if pager_sec and "index.html#section-lessons" not in pager_sec.group(1):
        # Add index link in pager
        old_pager = pager_sec.group(1)
        prev_btn_m = re.search(r'(<a href="chapter\d+\.html"[^>]*>.*?</a>)', old_pager, re.DOTALL)
        if prev_btn_m:
            index_btn = '\n            <a href="index.html#section-lessons" class="bg-white/10 hover:bg-white/20 text-white px-4 py-2.5 rounded-xl text-xs font-bold border border-white/20 transition whitespace-nowrap flex-shrink-0 inline-flex items-center gap-1.5 shadow-sm">\n              <i class="fa-solid fa-list"></i> <span>สารบัญ</span>\n            </a>'
            new_pager = old_pager.replace(prev_btn_m.group(1), prev_btn_m.group(1) + index_btn)
            html = html.replace(old_pager, new_pager)
            modified = True
            print(f"Ch.{c:02d}: Added สารบัญ button to Pager")

    if modified:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Ch.{c:02d}: Successfully saved updates.")
    else:
        print(f"Ch.{c:02d}: Already in full compliance.")

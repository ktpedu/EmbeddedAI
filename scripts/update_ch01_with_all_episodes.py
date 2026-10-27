import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('web_learning_platform/public/chapter01.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Hero section to add the 5-episode shelf
hero_shelf = """
        <!-- Chapter 1 Video Episodes Shelf -->
        <div class="mt-4 p-4 bg-black/40 backdrop-blur-md rounded-2xl border border-white/15 max-w-3xl space-y-2.5">
          <div class="text-xs font-bold text-yellow-300 flex items-center justify-between">
            <span class="flex items-center gap-2"><i class="fa-brands fa-youtube text-red-500 text-base"></i> รวมสื่อวีดิทัศน์ประกอบการเรียนรู้ บทที่ 1 ครบทั้ง 5 ตอน (อ.ธนา):</span>
            <span class="text-[11px] text-slate-300 font-normal hidden sm:inline">คลิกเพื่อรับชมบนหน้านี้ได้ทันที</span>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2 text-xs">
            <button type="button" onclick="openVideoByEpisode(1, 'Ep.01')" class="p-2.5 rounded-xl bg-white/10 hover:bg-white/20 text-left text-slate-200 hover:text-white border border-white/10 transition flex items-center gap-2.5 group cursor-pointer">
              <span class="w-7 h-7 rounded-lg bg-red-600 text-white font-bold flex items-center justify-center text-xs shrink-0 group-hover:scale-105 transition-transform shadow"><i class="fa-solid fa-play"></i></span>
              <div class="min-w-0">
                <div class="font-bold text-white text-xs truncate">Ep.01: ติดตั้ง App Lab</div>
                <div class="text-[10px] text-yellow-300/80 truncate">Installing Arduino App Lab</div>
              </div>
            </button>
            <button type="button" onclick="openVideoByEpisode(1, 'Ep.02')" class="p-2.5 rounded-xl bg-white/10 hover:bg-white/20 text-left text-slate-200 hover:text-white border border-white/10 transition flex items-center gap-2.5 group cursor-pointer">
              <span class="w-7 h-7 rounded-lg bg-red-600 text-white font-bold flex items-center justify-center text-xs shrink-0 group-hover:scale-105 transition-transform shadow"><i class="fa-solid fa-play"></i></span>
              <div class="min-w-0">
                <div class="font-bold text-white text-xs truncate">Ep.02: ติดตั้ง Debian Linux</div>
                <div class="text-[10px] text-yellow-300/80 truncate">Debian Linux AArch64 OS</div>
              </div>
            </button>
            <button type="button" onclick="openVideoByEpisode(1, 'Ep.03')" class="p-2.5 rounded-xl bg-white/10 hover:bg-white/20 text-left text-slate-200 hover:text-white border border-white/10 transition flex items-center gap-2.5 group cursor-pointer">
              <span class="w-7 h-7 rounded-lg bg-red-600 text-white font-bold flex items-center justify-center text-xs shrink-0 group-hover:scale-105 transition-transform shadow"><i class="fa-solid fa-play"></i></span>
              <div class="min-w-0">
                <div class="font-bold text-white text-xs truncate">Ep.03: Initial Setup บอร์ด</div>
                <div class="text-[10px] text-yellow-300/80 truncate">Initial Setup for UNO Q</div>
              </div>
            </button>
            <button type="button" onclick="openVideoByEpisode(1, 'Ep.04')" class="p-2.5 rounded-xl bg-white/10 hover:bg-white/20 text-left text-slate-200 hover:text-white border border-white/10 transition flex items-center gap-2.5 group cursor-pointer">
              <span class="w-7 h-7 rounded-lg bg-red-600 text-white font-bold flex items-center justify-center text-xs shrink-0 group-hover:scale-105 transition-transform shadow"><i class="fa-solid fa-play"></i></span>
              <div class="min-w-0">
                <div class="font-bold text-white text-xs truncate">Ep.04: สร้าง App บน App Lab</div>
                <div class="text-[10px] text-yellow-300/80 truncate">Create App for UNO Q</div>
              </div>
            </button>
            <button type="button" onclick="openVideoByEpisode(1, 'Ep.29')" class="p-2.5 rounded-xl bg-white/10 hover:bg-white/20 text-left text-slate-200 hover:text-white border border-white/10 transition flex items-center gap-2.5 group cursor-pointer sm:col-span-2 lg:col-span-2">
              <span class="w-7 h-7 rounded-lg bg-red-600 text-white font-bold flex items-center justify-center text-xs shrink-0 group-hover:scale-105 transition-transform shadow"><i class="fa-solid fa-play"></i></span>
              <div class="min-w-0">
                <div class="font-bold text-white text-xs truncate">Ep.29: เริ่มต้นใช้งาน Edge Impulse</div>
                <div class="text-[10px] text-yellow-300/80 truncate">เริ่มต้นใช้งาน Edge Impulse เพื่อเทรนโมเดล AI</div>
              </div>
            </button>
          </div>
        </div>"""

if '<!-- Chapter 1 Video Episodes Shelf -->' not in content:
    # Insert right after the Quick Action Buttons </div>
    btn_div_end = content.find('<!-- Quick Lesson Meta Card -->')
    if btn_div_end != -1:
        # Find </div> right before <!-- Quick Lesson Meta Card -->
        pos = content.rfind('</div>', 0, btn_div_end)
        content = content[:pos] + hero_shelf + "\n      " + content[pos:]
        print("[OK] Inserted Hero 5-episode shelf into Chapter 1")

# 2. Add video button to Section 1
s1_old = """          <div class="border-b border-slate-100 pb-4">
            <span class="badge-ep text-xs font-black px-3 py-1 rounded-full uppercase tracking-wider">
              <i class="fa-solid fa-laptop-code mr-1 text-yellow-400"></i> ตอนที่ 1: การติดตั้งซอฟต์แวร์
            </span>
            <h2 class="text-2xl font-black text-[#173b6b] font-heading mt-2">
              การติดตั้งและตั้งค่าโปรแกรมสภาพแวดล้อม Arduino App Lab
            </h2>
          </div>"""

s1_new = """          <div class="border-b border-slate-100 pb-4 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
            <div>
              <span class="badge-ep text-xs font-black px-3 py-1 rounded-full uppercase tracking-wider">
                <i class="fa-solid fa-laptop-code mr-1 text-yellow-400"></i> ตอนที่ 1: การติดตั้งซอฟต์แวร์
              </span>
              <h2 class="text-2xl font-black text-[#173b6b] font-heading mt-2">
                การติดตั้งและตั้งค่าโปรแกรมสภาพแวดล้อม Arduino App Lab
              </h2>
            </div>
            <button type="button" onclick="openVideoByEpisode(1, 'Ep.01')" class="self-start sm:self-auto shrink-0 px-3.5 py-2 rounded-xl bg-red-600 hover:bg-red-700 text-white text-xs font-bold shadow flex items-center gap-2 transition cursor-pointer" title="คลิกเพื่อเปิดดูคลิป Ep.01 บนหน้านี้">
              <i class="fa-brands fa-youtube"></i> ดูคลิป Ep.01 (ติดตั้ง App Lab)
            </button>
          </div>"""

if s1_old in content:
    content = content.replace(s1_old, s1_new)
    print("[OK] Added video button to Section 1 (Ep.01)")

# 3. Add video button to Section 2
s2_old = """          <div class="border-b border-slate-100 pb-4">
            <span class="badge-ep text-xs font-black px-3 py-1 rounded-full uppercase tracking-wider">
              <i class="fa-brands fa-linux mr-1 text-yellow-400"></i> ตอนที่ 2: สถาปัตยกรรมและการตรวจสอบระบบปฏิบัติการ
            </span>
            <h2 class="text-2xl font-black text-[#173b6b] font-heading mt-2">
              สถาปัตยกรรมระบบและการตรวจสอบระบบปฏิบัติการ Debian Linux AArch64 บนบอร์ดพัฒนา
            </h2>
          </div>"""

s2_new = """          <div class="border-b border-slate-100 pb-4 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
            <div>
              <span class="badge-ep text-xs font-black px-3 py-1 rounded-full uppercase tracking-wider">
                <i class="fa-brands fa-linux mr-1 text-yellow-400"></i> ตอนที่ 2: สถาปัตยกรรมและการตรวจสอบระบบปฏิบัติการ
              </span>
              <h2 class="text-2xl font-black text-[#173b6b] font-heading mt-2">
                สถาปัตยกรรมระบบและการตรวจสอบระบบปฏิบัติการ Debian Linux AArch64 บนบอร์ดพัฒนา
              </h2>
            </div>
            <button type="button" onclick="openVideoByEpisode(1, 'Ep.02')" class="self-start sm:self-auto shrink-0 px-3.5 py-2 rounded-xl bg-red-600 hover:bg-red-700 text-white text-xs font-bold shadow flex items-center gap-2 transition cursor-pointer" title="คลิกเพื่อเปิดดูคลิป Ep.02 บนหน้านี้">
              <i class="fa-brands fa-youtube"></i> ดูคลิป Ep.02 (Debian Linux บน UNO Q)
            </button>
          </div>"""

if s2_old in content:
    content = content.replace(s2_old, s2_new)
    print("[OK] Added video button to Section 2 (Ep.02)")

# 4. Add video button to Section 3
s3_old = """          <div class="border-b border-slate-100 pb-4">
            <span class="badge-ep text-xs font-black px-3 py-1 rounded-full uppercase tracking-wider">
              <i class="fa-solid fa-wifi mr-1 text-yellow-400"></i> ตอนที่ 3: การเชื่อมต่อระบบเครือข่าย
            </span>
            <h2 class="text-2xl font-black text-[#173b6b] font-heading mt-2">
              การเชื่อมต่อและการตั้งค่าโหมดเครือข่าย (Network Mode)
            </h2>
          </div>"""

s3_new = """          <div class="border-b border-slate-100 pb-4 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
            <div>
              <span class="badge-ep text-xs font-black px-3 py-1 rounded-full uppercase tracking-wider">
                <i class="fa-solid fa-wifi mr-1 text-yellow-400"></i> ตอนที่ 3: การเชื่อมต่อระบบเครือข่าย
              </span>
              <h2 class="text-2xl font-black text-[#173b6b] font-heading mt-2">
                การเชื่อมต่อและการตั้งค่าโหมดเครือข่าย (Network Mode)
              </h2>
            </div>
            <button type="button" onclick="openVideoByEpisode(1, 'Ep.03')" class="self-start sm:self-auto shrink-0 px-3.5 py-2 rounded-xl bg-red-600 hover:bg-red-700 text-white text-xs font-bold shadow flex items-center gap-2 transition cursor-pointer" title="คลิกเพื่อเปิดดูคลิป Ep.03 บนหน้านี้">
              <i class="fa-brands fa-youtube"></i> ดูคลิป Ep.03 (Initial Setup บอร์ด)
            </button>
          </div>"""

if s3_old in content:
    content = content.replace(s3_old, s3_new)
    print("[OK] Added video button to Section 3 (Ep.03)")

# 5. Add video buttons to Section 4
s4_old = """          <div class="border-b border-slate-100 pb-4">
            <span class="badge-ep text-xs font-black px-3 py-1 rounded-full uppercase tracking-wider">
              <i class="fa-solid fa-brain mr-1 text-yellow-400"></i> ตอนที่ 4: สถาปัตยกรรมปัญญาประดิษฐ์บนอุปกรณ์ปลายทาง
            </span>
            <h2 class="text-2xl font-black text-[#173b6b] font-heading mt-2">
              หลักการปัญญาประดิษฐ์บนอุปกรณ์ปลายทาง และการใช้งานแพลตฟอร์ม Edge Impulse
            </h2>
          </div>"""

s4_new = """          <div class="border-b border-slate-100 pb-4 flex flex-col lg:flex-row lg:items-center lg:justify-between gap-3">
            <div>
              <span class="badge-ep text-xs font-black px-3 py-1 rounded-full uppercase tracking-wider">
                <i class="fa-solid fa-brain mr-1 text-yellow-400"></i> ตอนที่ 4: สถาปัตยกรรมปัญญาประดิษฐ์บนอุปกรณ์ปลายทาง
              </span>
              <h2 class="text-2xl font-black text-[#173b6b] font-heading mt-2">
                หลักการปัญญาประดิษฐ์บนอุปกรณ์ปลายทาง และการใช้งานแพลตฟอร์ม Edge Impulse
              </h2>
            </div>
            <div class="flex flex-wrap items-center gap-2 shrink-0">
              <button type="button" onclick="openVideoByEpisode(1, 'Ep.04')" class="px-3 py-2 rounded-xl bg-red-600 hover:bg-red-700 text-white text-xs font-bold shadow flex items-center gap-1.5 transition cursor-pointer" title="คลิกเพื่อเปิดดูคลิป Ep.04 บนหน้านี้">
                <i class="fa-brands fa-youtube"></i> ดูคลิป Ep.04 (สร้าง App)
              </button>
              <button type="button" onclick="openVideoByEpisode(1, 'Ep.29')" class="px-3 py-2 rounded-xl bg-red-600 hover:bg-red-700 text-white text-xs font-bold shadow flex items-center gap-1.5 transition cursor-pointer" title="คลิกเพื่อเปิดดูคลิป Ep.29 บนหน้านี้">
                <i class="fa-brands fa-youtube"></i> ดูคลิป Ep.29 (Edge Impulse)
              </button>
            </div>
          </div>"""

if s4_old in content:
    content = content.replace(s4_old, s4_new)
    print("[OK] Added video buttons to Section 4 (Ep.04 & Ep.29)")

with open('web_learning_platform/public/chapter01.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("[DONE] Successfully updated chapter01.html with full episode videos")

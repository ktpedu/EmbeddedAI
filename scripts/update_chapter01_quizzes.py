# -*- coding: utf-8 -*-
"""
Script to update Chapter 1 quizzes across the database and markdown files.
"""
import os
import sys
import json

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

new_quizzes = [
  {
    "id": "q_ch01_01",
    "quiz_uid": 1,
    "chapter_id": "ch01",
    "category": "chapter_quiz",
    "chapter_number": 1,
    "question_type": "multiple_choice",
    "question_text": "ข้อใดอธิบายจุดเด่นสำคัญของการประมวลผลปัญญาประดิษฐ์บนอุปกรณ์ปลายทาง (Edge AI) เมื่อเปรียบเทียบกับระบบคลาวด์ (Cloud AI) ได้ถูกต้องที่สุด",
    "options": [
      "บอร์ดปลายทางสามารถเก็บข้อมูลภาพและเสียงย้อนหลังได้ไม่จำกัดโดยไม่ต้องลบ",
      "ตอบสนองได้รวดเร็วทันที มีความหน่วงต่ำมาก (Low Latency) และทำงานได้ต่อเนื่องแม้ไม่มีสัญญาณอินเทอร์เน็ต",
      "ไม่จำเป็นต้องจัดเตรียมข้อมูลหรือฝึกสอนโมเดลก่อนนำมาใช้งาน",
      "สามารถประมวลผลโมเดลขนาดใหญ่ที่มีพารามิเตอร์ระดับแสนล้านได้เร็วกว่าคอมพิวเตอร์แม่ข่าย"
    ],
    "correct_index": 1,
    "correct_letter": "ข",
    "explanation": "จุดเด่นของ Edge AI คือประมวลผลบนตัวบอร์ดได้ทันที มีความหน่วงต่ำ และทำงานแบบออฟไลน์ได้โดยไม่ต้องต่อเน็ตตลอดเวลา",
    "points": 1
  },
  {
    "id": "q_ch01_02",
    "quiz_uid": 2,
    "chapter_id": "ch01",
    "category": "chapter_quiz",
    "chapter_number": 1,
    "question_type": "multiple_choice",
    "question_text": "บอร์ดพัฒนา Arduino UNO Q ใช้สถาปัตยกรรมประมวลผลร่วม (Heterogeneous Computing) ซึ่งเป็นการผสานการทำงานระหว่างหน่วยประมวลผลคู่ใด",
    "options": [
      "Intel Core i5 ทำงานร่วมกับชิป Raspberry Pi RP2040",
      "Qualcomm Dragonwing QRB2210 ทำงานร่วมกับไมโครคอนโทรลเลอร์ ARM Cortex-M4",
      "ATmega328P ทำงานร่วมกับชิปสื่อสารไร้สาย ESP8266",
      "Apple Silicon M1 ทำงานร่วมกับชิป STM32F401"
    ],
    "correct_index": 1,
    "correct_letter": "ข",
    "explanation": "บอร์ด Arduino UNO Q ผสานการทำงานระหว่างชิป MPU Qualcomm Dragonwing QRB2210 และไมโครคอนโทรลเลอร์ ARM Cortex-M4",
    "points": 1
  },
  {
    "id": "q_ch01_03",
    "quiz_uid": 3,
    "chapter_id": "ch01",
    "category": "chapter_quiz",
    "chapter_number": 1,
    "question_type": "multiple_choice",
    "question_text": "ระบบปฏิบัติการหลักที่ทำงานอยู่บนชิป Qualcomm Dragonwing QRB2210 ของบอร์ด Arduino UNO Q คือระบบปฏิบัติการใด",
    "options": [
      "FreeRTOS (สถาปัตยกรรม 16 บิต)",
      "Debian Linux (สถาปัตยกรรม AArch64)",
      "Windows 11 IoT Enterprise (สถาปัตยกรรม x86)",
      "Android Automotive OS (สถาปัตยกรรม ARMv7)"
    ],
    "correct_index": 1,
    "correct_letter": "ข",
    "explanation": "หน่วยประมวลผลหลักของบอร์ดรันระบบปฏิบัติการ Debian Linux บนสถาปัตยกรรม 64 บิต หรือ AArch64",
    "points": 1
  },
  {
    "id": "q_ch01_04",
    "quiz_uid": 4,
    "chapter_id": "ch01",
    "category": "chapter_quiz",
    "chapter_number": 1,
    "question_type": "multiple_choice",
    "question_text": "ขณะจ่ายกระแสไฟฟ้าเข้าสู่บอร์ด Arduino UNO Q หากไฟแสดงสถานะดวงใด \"กะพริบเป็นจังหวะ\" จะหมายถึงซีพียูกำลังโหลดระบบปฏิบัติการลีนุกซ์เข้าสู่ระบบ (Booting)",
    "options": [
      "ไฟแสดงสถานะ PWR (สีเขียว)",
      "ไฟแสดงสถานะ BOOT/ACT (สีส้ม/เหลือง)",
      "ไฟแสดงสถานะ SYS OK (สีน้ำเงิน)",
      "ไฟแสดงสถานะ RX/TX (สีขาว)"
    ],
    "correct_index": 1,
    "correct_letter": "ข",
    "explanation": "ไฟ BOOT/ACT จะกะพริบเป็นจังหวะขณะระบบกำลังโหลดระบบปฏิบัติการ และไฟ SYS OK จะติดสว่างเมื่อระบบพร้อมใช้งาน",
    "points": 1
  },
  {
    "id": "q_ch01_05",
    "quiz_uid": 5,
    "chapter_id": "ch01",
    "category": "chapter_quiz",
    "chapter_number": 1,
    "question_type": "multiple_choice",
    "question_text": "เมื่อเปิดหน้าต่างเทอร์มินัล (Linux Terminal) บนบอร์ด Arduino UNO Q หากต้องการตรวจสอบว่าระบบทำงานอยู่บนสถาปัตยกรรม 64 บิต (aarch64) หรือไม่ ควรใช้คำสั่งใด",
    "options": [
      "ping arduino-uno-q.local",
      "free -h",
      "uname -a",
      "mkdir ei-models"
    ],
    "correct_index": 2,
    "correct_letter": "ค",
    "explanation": "คำสั่ง uname -a หรือ uname -m ใช้ตรวจสอบข้อมูลเคอร์เนลและสถาปัตยกรรมระบบ ซึ่งจะแสดงผลเป็น aarch64",
    "points": 1
  },
  {
    "id": "q_ch01_06",
    "quiz_uid": 6,
    "chapter_id": "ch01",
    "category": "chapter_quiz",
    "chapter_number": 1,
    "question_type": "multiple_choice",
    "question_text": "โปรแกรมสภาพแวดล้อมสำหรับการพัฒนา (IDE) ที่ออกแบบมาเพื่อบอร์ดตระกูล Q-Series โดยเน้นการเขียนโค้ดภาษาไพทอนและระบบโมดูลบล็อกคำสั่ง (Modular Brick) คือโปรแกรมใด",
    "options": [
      "Arduino IDE 1.8",
      "Arduino App Lab",
      "Thonny Python IDE",
      "Visual Studio Code Community"
    ],
    "correct_index": 1,
    "correct_letter": "ข",
    "explanation": "Arduino App Lab เป็นโปรแกรมพัฒนาหลักของบอร์ด Q-Series ที่ใช้ Python 3 ร่วมกับสถาปัตยกรรม Modular Brick",
    "points": 1
  },
  {
    "id": "q_ch01_07",
    "quiz_uid": 7,
    "chapter_id": "ch01",
    "category": "chapter_quiz",
    "chapter_number": 1,
    "question_type": "multiple_choice",
    "question_text": "ในการเชื่อมต่อบอร์ด Arduino UNO Q เข้ากับเครือข่ายไร้สาย (Wi-Fi) นักเรียนสามารถเรียกเข้าใช้งานบอร์ดได้ผ่านชื่อโฮสต์ (Hostname) ใด โดยไม่จำเป็นต้องจดจำหมายเลข IP Address",
    "options": [
      "arduino.cc",
      "uno-q-board.net",
      "arduino-uno-q.local",
      "edge-impulse.local"
    ],
    "correct_index": 2,
    "correct_letter": "ค",
    "explanation": "ระบบรองรับโปรโตคอล mDNS ทำให้เรียกชื่อเครื่องเป็น arduino-uno-q.local ในเครือข่ายเดียวกันได้ทันที",
    "points": 1
  },
  {
    "id": "q_ch01_08",
    "quiz_uid": 8,
    "chapter_id": "ch01",
    "category": "chapter_quiz",
    "chapter_number": 1,
    "question_type": "multiple_choice",
    "question_text": "สายเชื่อมต่อที่จำเป็นต้องใช้สำหรับการจ่ายพลังงานไฟฟ้าและรับส่งข้อมูลระหว่างคอมพิวเตอร์กับบอร์ด Arduino UNO Q ควรเป็นสายประเภทใด",
    "options": [
      "สาย USB Micro-B ชนิดชาร์จไฟได้อย่างเดียว",
      "สาย USB Type-C ชนิดที่รองรับทั้งการรับส่งข้อมูลและจ่ายกระแสไฟฟ้าได้ 3A",
      "สายสัญญาณภาพ HDMI แบบหัวแปลงคู่",
      "สายสัญญาณเสียงแจ็ค 3.5 มิลลิเมตร"
    ],
    "correct_index": 1,
    "correct_letter": "ข",
    "explanation": "บอร์ดต้องการสาย USB Type-C ที่รองรับการถ่ายโอนข้อมูล Data Sync ควบคู่กับการจ่ายกระแสไฟอย่างน้อย 3A เพื่อให้ระบบทำงานได้เสถียร",
    "points": 1
  },
  {
    "id": "q_ch01_09",
    "quiz_uid": 9,
    "chapter_id": "ch01",
    "category": "chapter_quiz",
    "chapter_number": 1,
    "question_type": "multiple_choice",
    "question_text": "ไฟล์แบบจำลองปัญญาประดิษฐ์ที่คอมไพล์จากแพลตฟอร์ม Edge Impulse เพื่อนำมาสั่งประมวลผลบนระบบลีนุกซ์ของบอร์ด Arduino UNO Q จะมีนามสกุลไฟล์ตามข้อใด",
    "options": [
      "`.eim`",
      "`.ino`",
      "`.hex`",
      "`.exe`"
    ],
    "correct_index": 0,
    "correct_letter": "ก",
    "explanation": "ไฟล์ไบนารีโมเดลสำหรับรันบนระบบลีนุกซ์ของ Edge Impulse คือไฟล์นามสกุล .eim ย่อมาจาก Edge Impulse Model",
    "points": 1
  },
  {
    "id": "q_ch01_10",
    "quiz_uid": 10,
    "chapter_id": "ch01",
    "category": "chapter_quiz",
    "chapter_number": 1,
    "question_type": "multiple_choice",
    "question_text": "ในขั้นตอนการจัดการข้อมูล (Data Acquisition) บนแพลตฟอร์ม Edge Impulse เหตุใดจึงต้องแบ่งชุดข้อมูลออกเป็นชุดฝึกสอน (Training Set 80%) และชุดทดสอบ (Testing Set 20%)",
    "options": [
      "เพื่อบีบอัดขนาดไฟล์รูปภาพให้เล็กลงครึ่งหนึ่ง",
      "เพื่อให้ระบบสามารถส่งข้อมูลผ่านเครือข่าย Wi-Fi ได้เร็วขึ้น",
      "เพื่อแยกข้อมูลส่วนหนึ่งไว้ทดสอบความแม่นยำจริง ป้องกันปัญหาโมเดลท่องจำข้อมูลเดิม (Overfitting)",
      "เพื่อแปลงข้อมูลสัญญาณเสียงดิจิทัลให้เป็นข้อมูลภาพความร้อน"
    ],
    "correct_index": 2,
    "correct_letter": "ค",
    "explanation": "การแยกข้อมูล Testing 20% ไว้ต่างหาก มีไว้เพื่อประเมินผลกับข้อมูลใหม่ที่โมเดลไม่เคยเห็นในตอนฝึกสอน เพื่อป้องกันปัญหา Overfitting",
    "points": 1
  }
]

def update_json_files():
    targets = [
        os.path.join('web_learning_platform', 'data', 'db.json'),
        os.path.join('web_learning_platform', 'data', 'seed.json'),
        os.path.join('web_learning_platform', 'data', 'db.backup.json')
    ]
    for target in targets:
        if os.path.exists(target):
            with open(target, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            quizzes = data.get('quizzes', [])
            # Keep other chapters
            remaining = [q for q in quizzes if not (q.get('chapter_id') == 'ch01' or (q.get('category') == 'chapter_quiz' and q.get('chapter_number') == 1))]
            data['quizzes'] = new_quizzes + remaining
            
            with open(target, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"[OK] Updated {target} -> Total quizzes: {len(data['quizzes'])}")

def update_120_markdown():
    path = 'ข้อสอบปรนัย_แยกรายบท_120ข้อ.md'
    if not os.path.exists(path):
        return
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Locate chapter 1 section up to chapter 2
    # The header starts with:
    # # แบบทดสอบปรนัยแยกรายบท: ปัญญาประดิษฐ์บนระบบสมองกลฝังตัว
    # ...
    # # แบบทดสอบประจำบทที่ 1: เริ่มต้นใช้งาน Edge Impulse เพื่อเทรนโมเดล AI
    
    start_marker = "แบบทดสอบประจำบทที่ 1"
    end_marker = "# แบบทดสอบประจำบทที่ 2"
    
    p1 = content.find(start_marker)
    p2 = content.find(end_marker)
    
    if p1 != -1 and p2 != -1:
        # find the line start of start_marker
        line_start = content.rfind('\n', 0, p1)
        if line_start == -1:
            line_start = 0
        else:
            line_start += 1
            
        new_ch1_content = """# แบบทดสอบประจำบทที่ 1: การเตรียมความพร้อมระบบและบอร์ดพัฒนา Arduino UNO Q
**จำนวนข้อสอบ:** 10 ข้อ (แบบเลือกตอบ 4 ตัวเลือก ก, ข, ค, ง) | **เวลาในการทำแบบทดสอบ:** 20 นาที | **คะแนนเต็ม:** 10 คะแนน

#### 1. ข้อใดอธิบายจุดเด่นสำคัญของการประมวลผลปัญญาประดิษฐ์บนอุปกรณ์ปลายทาง (Edge AI) เมื่อเปรียบเทียบกับระบบคลาวด์ (Cloud AI) ได้ถูกต้องที่สุด
ก. บอร์ดปลายทางสามารถเก็บข้อมูลภาพและเสียงย้อนหลังได้ไม่จำกัดโดยไม่ต้องลบ  
ข. ตอบสนองได้รวดเร็วทันที มีความหน่วงต่ำมาก (Low Latency) และทำงานได้ต่อเนื่องแม้ไม่มีสัญญาณอินเทอร์เน็ต  
ค. ไม่จำเป็นต้องจัดเตรียมข้อมูลหรือฝึกสอนโมเดลก่อนนำมาใช้งาน  
ง. สามารถประมวลผลโมเดลขนาดใหญ่ที่มีพารามิเตอร์ระดับแสนล้านได้เร็วกว่าคอมพิวเตอร์แม่ข่าย  

#### 2. บอร์ดพัฒนา Arduino UNO Q ใช้สถาปัตยกรรมประมวลผลร่วม (Heterogeneous Computing) ซึ่งเป็นการผสานการทำงานระหว่างหน่วยประมวลผลคู่ใด
ก. Intel Core i5 ทำงานร่วมกับชิป Raspberry Pi RP2040  
ข. Qualcomm Dragonwing QRB2210 ทำงานร่วมกับไมโครคอนโทรลเลอร์ ARM Cortex-M4  
ค. ATmega328P ทำงานร่วมกับชิปสื่อสารไร้สาย ESP8266  
ง. Apple Silicon M1 ทำงานร่วมกับชิป STM32F401  

#### 3. ระบบปฏิบัติการหลักที่ทำงานอยู่บนชิป Qualcomm Dragonwing QRB2210 ของบอร์ด Arduino UNO Q คือระบบปฏิบัติการใด
ก. FreeRTOS (สถาปัตยกรรม 16 บิต)  
ข. Debian Linux (สถาปัตยกรรม AArch64)  
ค. Windows 11 IoT Enterprise (สถาปัตยกรรม x86)  
ง. Android Automotive OS (สถาปัตยกรรม ARMv7)  

#### 4. ขณะจ่ายกระแสไฟฟ้าเข้าสู่บอร์ด Arduino UNO Q หากไฟแสดงสถานะดวงใด "กะพริบเป็นจังหวะ" จะหมายถึงซีพียูกำลังโหลดระบบปฏิบัติการลีนุกซ์เข้าสู่ระบบ (Booting)
ก. ไฟแสดงสถานะ PWR (สีเขียว)  
ข. ไฟแสดงสถานะ BOOT/ACT (สีส้ม/เหลือง)  
ค. ไฟแสดงสถานะ SYS OK (สีน้ำเงิน)  
ง. ไฟแสดงสถานะ RX/TX (สีขาว)  

#### 5. เมื่อเปิดหน้าต่างเทอร์มินัล (Linux Terminal) บนบอร์ด Arduino UNO Q หากต้องการตรวจสอบว่าระบบทำงานอยู่บนสถาปัตยกรรม 64 บิต (aarch64) หรือไม่ ควรใช้คำสั่งใด
ก. `ping arduino-uno-q.local`  
ข. `free -h`  
ค. `uname -a`  
ง. `mkdir ei-models`  

#### 6. โปรแกรมสภาพแวดล้อมสำหรับการพัฒนา (IDE) ที่ออกแบบมาเพื่อบอร์ดตระกูล Q-Series โดยเน้นการเขียนโค้ดภาษาไพทอนและระบบโมดูลบล็อกคำสั่ง (Modular Brick) คือโปรแกรมใด
ก. Arduino IDE 1.8  
ข. Arduino App Lab  
ค. Thonny Python IDE  
ง. Visual Studio Code Community  

#### 7. ในการเชื่อมต่อบอร์ด Arduino UNO Q เข้ากับเครือข่ายไร้สาย (Wi-Fi) นักเรียนสามารถเรียกเข้าใช้งานบอร์ดได้ผ่านชื่อโฮสต์ (Hostname) ใด โดยไม่จำเป็นต้องจดจำหมายเลข IP Address
ก. `arduino.cc`  
ข. `uno-q-board.net`  
ค. `arduino-uno-q.local`  
ง. `edge-impulse.local`  

#### 8. สายเชื่อมต่อที่จำเป็นต้องใช้สำหรับการจ่ายพลังงานไฟฟ้าและรับส่งข้อมูลระหว่างคอมพิวเตอร์กับบอร์ด Arduino UNO Q ควรเป็นสายประเภทใด
ก. สาย USB Micro-B ชนิดชาร์จไฟได้อย่างเดียว  
ข. สาย USB Type-C ชนิดที่รองรับทั้งการรับส่งข้อมูลและจ่ายกระแสไฟฟ้าได้ 3A  
ค. สายสัญญาณภาพ HDMI แบบหัวแปลงคู่  
ง. สายสัญญาณเสียงแจ็ค 3.5 มิลลิเมตร  

#### 9. ไฟล์แบบจำลองปัญญาประดิษฐ์ที่คอมไพล์จากแพลตฟอร์ม Edge Impulse เพื่อนำมาสั่งประมวลผลบนระบบลีนุกซ์ของบอร์ด Arduino UNO Q จะมีนามสกุลไฟล์ตามข้อใด
ก. `.eim`  
ข. `.ino`  
ค. `.hex`  
ง. `.exe`  

#### 10. ในขั้นตอนการจัดการข้อมูล (Data Acquisition) บนแพลตฟอร์ม Edge Impulse เหตุใดจึงต้องแบ่งชุดข้อมูลออกเป็นชุดฝึกสอน (Training Set 80%) และชุดทดสอบ (Testing Set 20%)
ก. เพื่อบีบอัดขนาดไฟล์รูปภาพให้เล็กลงครึ่งหนึ่ง  
ข. เพื่อให้ระบบสามารถส่งข้อมูลผ่านเครือข่าย Wi-Fi ได้เร็วขึ้น  
ค. เพื่อแยกข้อมูลส่วนหนึ่งไว้ทดสอบความแม่นยำจริง ป้องกันปัญหาโมเดลท่องจำข้อมูลเดิม (Overfitting)  
ง. เพื่อแปลงข้อมูลสัญญาณเสียงดิจิทัลให้เป็นข้อมูลภาพความร้อน  

---

### เฉลยคำตอบประจำบทที่ 1
1. **ข.** (จุดเด่นของ Edge AI คือประมวลผลบนตัวบอร์ดได้ทันที มีความหน่วงต่ำ และทำงานแบบออฟไลน์ได้โดยไม่ต้องต่อเน็ตตลอดเวลา)
2. **ข.** (บอร์ด Arduino UNO Q ผสานการทำงานระหว่างชิป MPU Qualcomm Dragonwing QRB2210 และไมโครคอนโทรลเลอร์ ARM Cortex-M4)
3. **ข.** (หน่วยประมวลผลหลักของบอร์ดรันระบบปฏิบัติการ Debian Linux บนสถาปัตยกรรม 64 บิต หรือ AArch64)
4. **ข.** (ไฟ BOOT/ACT จะกะพริบเป็นจังหวะขณะระบบกำลังโหลดระบบปฏิบัติการ และไฟ SYS OK จะติดสว่างเมื่อระบบพร้อมใช้งาน)
5. **ค.** (คำสั่ง `uname -a` หรือ `uname -m` ใช้ตรวจสอบข้อมูลเคอร์เนลและสถาปัตยกรรมระบบ ซึ่งจะแสดงผลเป็น `aarch64`)
6. **ข.** (Arduino App Lab เป็นโปรแกรมพัฒนาหลักของบอร์ด Q-Series ที่ใช้ Python 3 ร่วมกับสถาปัตยกรรม Modular Brick)
7. **ค.** (ระบบรองรับโปรโตคอล mDNS ทำให้เรียกชื่อเครื่องเป็น `arduino-uno-q.local` ในเครือข่ายเดียวกันได้ทันที)
8. **ข.** (บอร์ดต้องการสาย USB Type-C ที่รองรับการถ่ายโอนข้อมูล Data Sync ควบคู่กับการจ่ายกระแสไฟอย่างน้อย 3A เพื่อให้ระบบทำงานได้เสถียร)
9. **ก.** (ไฟล์ไบนารีโมเดลสำหรับรันบนระบบลีนุกซ์ของ Edge Impulse คือไฟล์นามสกุล `.eim` ย่อมาจาก Edge Impulse Model)
10. **ค.** (การแยกข้อมูล Testing 20% ไว้ต่างหาก มีไว้เพื่อประเมินผลกับข้อมูลใหม่ที่โมเดลไม่เคยเห็นในตอนฝึกสอน เพื่อป้องกันปัญหา Overfitting)

---

"""
        new_content = content[:line_start] + new_ch1_content + content[p2:]
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"[OK] Updated {path}")
    else:
        print(f"[!] Could not locate markers in {path}: p1={p1}, p2={p2}")

def update_bank_markdown():
    path = 'คลังข้อสอบปรนัย_ปัญญาประดิษฐ์สมองกลฝังตัว_รายบท.md'
    if not os.path.exists(path):
        return
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    start_marker = "กลุ่มบทเรียนที่ 1:"
    end_marker = "# กลุ่มบทเรียนที่ 2:"
    
    p1 = content.find(start_marker)
    p2 = content.find(end_marker)
    
    if p1 != -1 and p2 != -1:
        line_start = content.rfind('\n', 0, p1)
        if line_start == -1:
            line_start = 0
        else:
            line_start += 1
            
        new_ch1_bank = """# กลุ่มบทเรียนที่ 1: การเตรียมความพร้อมระบบและบอร์ดพัฒนา Arduino UNO Q

#### 1. ข้อใดอธิบายจุดเด่นสำคัญของการประมวลผลปัญญาประดิษฐ์บนอุปกรณ์ปลายทาง (Edge AI) เมื่อเปรียบเทียบกับระบบคลาวด์ (Cloud AI) ได้ถูกต้องที่สุด
ก. บอร์ดปลายทางสามารถเก็บข้อมูลภาพและเสียงย้อนหลังได้ไม่จำกัดโดยไม่ต้องลบ  
ข. ตอบสนองได้รวดเร็วทันที มีความหน่วงต่ำมาก (Low Latency) และทำงานได้ต่อเนื่องแม้ไม่มีสัญญาณอินเทอร์เน็ต  
ค. ไม่จำเป็นต้องจัดเตรียมข้อมูลหรือฝึกสอนโมเดลก่อนนำมาใช้งาน  
ง. สามารถประมวลผลโมเดลขนาดใหญ่ที่มีพารามิเตอร์ระดับแสนล้านได้เร็วกว่าคอมพิวเตอร์แม่ข่าย  

#### 2. บอร์ดพัฒนา Arduino UNO Q ใช้สถาปัตยกรรมประมวลผลร่วม (Heterogeneous Computing) ซึ่งเป็นการผสานการทำงานระหว่างหน่วยประมวลผลคู่ใด
ก. Intel Core i5 ทำงานร่วมกับชิป Raspberry Pi RP2040  
ข. Qualcomm Dragonwing QRB2210 ทำงานร่วมกับไมโครคอนโทรลเลอร์ ARM Cortex-M4  
ค. ATmega328P ทำงานร่วมกับชิปสื่อสารไร้สาย ESP8266  
ง. Apple Silicon M1 ทำงานร่วมกับชิป STM32F401  

#### 3. ระบบปฏิบัติการหลักที่ทำงานอยู่บนชิป Qualcomm Dragonwing QRB2210 ของบอร์ด Arduino UNO Q คือระบบปฏิบัติการใด
ก. FreeRTOS (สถาปัตยกรรม 16 บิต)  
ข. Debian Linux (สถาปัตยกรรม AArch64)  
ค. Windows 11 IoT Enterprise (สถาปัตยกรรม x86)  
ง. Android Automotive OS (สถาปัตยกรรม ARMv7)  

#### 4. ขณะจ่ายกระแสไฟฟ้าเข้าสู่บอร์ด Arduino UNO Q หากไฟแสดงสถานะดวงใด "กะพริบเป็นจังหวะ" จะหมายถึงซีพียูกำลังโหลดระบบปฏิบัติการลีนุกซ์เข้าสู่ระบบ (Booting)
ก. ไฟแสดงสถานะ PWR (สีเขียว)  
ข. ไฟแสดงสถานะ BOOT/ACT (สีส้ม/เหลือง)  
ค. ไฟแสดงสถานะ SYS OK (สีน้ำเงิน)  
ง. ไฟแสดงสถานะ RX/TX (สีขาว)  

#### 5. เมื่อเปิดหน้าต่างเทอร์มินัล (Linux Terminal) บนบอร์ด Arduino UNO Q หากต้องการตรวจสอบว่าระบบทำงานอยู่บนสถาปัตยกรรม 64 บิต (aarch64) หรือไม่ ควรใช้คำสั่งใด
ก. `ping arduino-uno-q.local`  
ข. `free -h`  
ค. `uname -a`  
ง. `mkdir ei-models`  

#### 6. โปรแกรมสภาพแวดล้อมสำหรับการพัฒนา (IDE) ที่ออกแบบมาเพื่อบอร์ดตระกูล Q-Series โดยเน้นการเขียนโค้ดภาษาไพทอนและระบบโมดูลบล็อกคำสั่ง (Modular Brick) คือโปรแกรมใด
ก. Arduino IDE 1.8  
ข. Arduino App Lab  
ค. Thonny Python IDE  
ง. Visual Studio Code Community  

#### 7. ในการเชื่อมต่อบอร์ด Arduino UNO Q เข้ากับเครือข่ายไร้สาย (Wi-Fi) นักเรียนสามารถเรียกเข้าใช้งานบอร์ดได้ผ่านชื่อโฮสต์ (Hostname) ใด โดยไม่จำเป็นต้องจดจำหมายเลข IP Address
ก. `arduino.cc`  
ข. `uno-q-board.net`  
ค. `arduino-uno-q.local`  
ง. `edge-impulse.local`  

#### 8. สายเชื่อมต่อที่จำเป็นต้องใช้สำหรับการจ่ายพลังงานไฟฟ้าและรับส่งข้อมูลระหว่างคอมพิวเตอร์กับบอร์ด Arduino UNO Q ควรเป็นสายประเภทใด
ก. สาย USB Micro-B ชนิดชาร์จไฟได้อย่างเดียว  
ข. สาย USB Type-C ชนิดที่รองรับทั้งการรับส่งข้อมูลและจ่ายกระแสไฟฟ้าได้ 3A  
ค. สายสัญญาณภาพ HDMI แบบหัวแปลงคู่  
ง. สายสัญญาณเสียงแจ็ค 3.5 มิลลิเมตร  

#### 9. ไฟล์แบบจำลองปัญญาประดิษฐ์ที่คอมไพล์จากแพลตฟอร์ม Edge Impulse เพื่อนำมาสั่งประมวลผลบนระบบลีนุกซ์ของบอร์ด Arduino UNO Q จะมีนามสกุลไฟล์ตามข้อใด
ก. `.eim`  
ข. `.ino`  
ค. `.hex`  
ง. `.exe`  

#### 10. ในขั้นตอนการจัดการข้อมูล (Data Acquisition) บนแพลตฟอร์ม Edge Impulse เหตุใดจึงต้องแบ่งชุดข้อมูลออกเป็นชุดฝึกสอน (Training Set 80%) และชุดทดสอบ (Testing Set 20%)
ก. เพื่อบีบอัดขนาดไฟล์รูปภาพให้เล็กลงครึ่งหนึ่ง  
ข. เพื่อให้ระบบสามารถส่งข้อมูลผ่านเครือข่าย Wi-Fi ได้เร็วขึ้น  
ค. เพื่อแยกข้อมูลส่วนหนึ่งไว้ทดสอบความแม่นยำจริง ป้องกันปัญหาโมเดลท่องจำข้อมูลเดิม (Overfitting)  
ง. เพื่อแปลงข้อมูลสัญญาณเสียงดิจิทัลให้เป็นข้อมูลภาพความร้อน  

---

### เฉลยคำตอบและคำอธิบาย กลุ่มบทเรียนที่ 1

1. **เฉลย ข.**  
   *คำอธิบาย:* ข้อได้เปรียบหลักของ Edge AI คือการประมวลผลได้ทันทีที่ตัวอุปกรณ์ จึงมีความหน่วงเวลาต่ำ (Low Latency) ตอบสนองได้แบบเรียลไทม์ ทำงานได้ต่อเนื่องในพื้นที่ที่ไม่มีสัญญาณอินเทอร์เน็ต และรักษาความเป็นส่วนตัวของข้อมูล
2. **เฉลย ข.**  
   *คำอธิบาย:* บอร์ด Arduino UNO Q ใช้สถาปัตยกรรมประมวลผลร่วม (Heterogeneous Computing) โดยผสาน MPU Qualcomm Dragonwing QRB2210 เข้ากับไมโครคอนโทรลเลอร์ ARM Cortex-M4
3. **เฉลย ข.**  
   *คำอธิบาย:* หน่วยประมวลผลหลักบนชิป Qualcomm รันระบบปฏิบัติการ Debian Linux บนสถาปัตยกรรม 64 บิต (AArch64)
4. **เฉลย ข.**  
   *คำอธิบาย:* สัญญาณไฟ BOOT/ACT จะกะพริบเป็นจังหวะเมื่อระบบปฏิบัติการลีนุกซ์กำลังถูกโหลดขึ้นมาทำงาน และเมื่อบูตเสร็จ ไฟ SYS OK จะติดสว่าง
5. **เฉลย ค.**  
   *คำอธิบาย:* คำสั่ง `uname -a` หรือ `uname -m` บน Bash Shell ใช้ตรวจสอบชื่อและสถาปัตยกรรมเคอร์เนล ซึ่งจะแสดงค่า `aarch64`
6. **เฉลย ข.**  
   *คำอธิบาย:* Arduino App Lab เป็นซอฟต์แวร์ IDE ยุคใหม่ที่พัฒนาขึ้นเพื่อรองรับบอร์ด Q-Series โดยใช้ภาษาไพทอนและระบบ Modular Brick
7. **เฉลย ค.**  
   *คำอธิบาย:* บอร์ดรองรับโปรโตคอล mDNS ซึ่งจะกระจายชื่อโฮสต์ในวงแลนเป็น `arduino-uno-q.local` ทำให้ค้นพบและเชื่อมต่อได้ทันที
8. **เฉลย ข.**  
   *คำอธิบาย:* การใช้งานบอร์ด Arduino UNO Q ให้เสถียร ต้องใช้สาย USB Type-C ที่รองรับการรับส่งข้อมูล (Data Sync) และรองรับการจ่ายกระแสไฟ 3A
9. **เฉลย ก.**  
   *คำอธิบาย:* ไฟล์ `.eim` (Edge Impulse Model) คือไฟล์ปฏิบัติการไบนารีที่คอมไพล์สำหรับระบบปฏิบัติการลีนุกซ์ AArch64
10. **เฉลย ค.**  
    *คำอธิบาย:* การแยก Testing Set ร้อยละ 20 ออกจาก Training Set เพื่อใช้ประเมินความสามารถในการวางนัยทั่วไป (Generalization) กับข้อมูลใหม่ และป้องกันปัญหาโมเดลท่องจำเฉพาะข้อมูลเดิม (Overfitting)

---

"""
        new_content = content[:line_start] + new_ch1_bank + content[p2:]
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"[OK] Updated {path}")
    else:
        print(f"[!] Could not locate markers in {path}: p1={p1}, p2={p2}")

if __name__ == '__main__':
    update_json_files()
    update_120_markdown()
    update_bank_markdown()

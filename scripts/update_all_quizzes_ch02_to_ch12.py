# -*- coding: utf-8 -*-
"""
Script to generate and update quizzes for Chapters 2 through 12 across:
1. web_learning_platform/data/db.json
2. web_learning_platform/data/seed.json
3. web_learning_platform/data/db.backup.json
4. ข้อสอบปรนัย_แยกรายบท_120ข้อ.md
5. คลังข้อสอบปรนัย_ปัญญาประดิษฐ์สมองกลฝังตัว_รายบท.md
"""
import os
import sys
import json

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Define all questions for Chapters 2 to 12 (10 questions each = 110 questions)
CHAPTER_QUIZZES = {
  2: [
    {
      "id": "q_ch02_01",
      "quiz_uid": 11,
      "chapter_id": "ch02",
      "category": "chapter_quiz",
      "chapter_number": 2,
      "question_type": "multiple_choice",
      "question_text": "ข้อใดอธิบายแนวคิดของสถาปัตยกรรม \"Modular Brick\" บนซอฟต์แวร์ Arduino App Lab ได้ถูกต้องที่สุด",
      "options": [
        "การเขียนชุดคำสั่งควบคุมอุปกรณ์ทั้งหมดรวมไว้ในฟังก์ชันเดียวแบบเดิม",
        "การออกแบบซอฟต์แวร์เป็นมอดูลอิสระที่แยกหน้าที่เฉพาะ และสามารถเชื่อมต่อแลกเปลี่ยนข้อมูลกันได้อย่างเป็นระบบ",
        "การต่อวงจรอิเล็กทรอนิกส์ด้วยตัวต่อของเล่นเพื่อทดสอบสัญญาณไฟฟ้า",
        "การเขียนโปรแกรมควบคุมคอมไพเลอร์ด้วยภาษาแอสเซมบลีโดยตรง"
      ],
      "correct_index": 1,
      "correct_letter": "ข",
      "explanation": "Modular Brick คือสถาปัตยกรรมซอฟต์แวร์ที่แบ่งหน้าที่การทำงานออกเป็นบล็อกมอดูลอิสระ ทำให้พัฒนา แก้ไข และนำกลับมาใช้ใหม่ได้ง่าย",
      "points": 1
    },
    {
      "id": "q_ch02_02",
      "quiz_uid": 12,
      "chapter_id": "ch02",
      "category": "chapter_quiz",
      "chapter_number": 2,
      "question_type": "multiple_choice",
      "question_text": "ในการพัฒนาแอปพลิเคชันด้วยภาษาไพทอนบน Arduino App Lab คำสั่ง App.run() ทำหน้าที่สำคัญตามข้อใด",
      "options": [
        "สั่งลบไฟล์ขยะทั้งหมดออกจากระบบปฏิบัติการลีนุกซ์",
        "เริ่มลูปการทำงานหลักของระบบและบริหารจัดการการทำงานของทุก Brick พร้อมกัน",
        "ปิดการทำงานของบอร์ดพัฒนาเพื่อประหยัดพลังงาน",
        "แปลงซอร์สโค้ดภาษาไพทอนให้กลายเป็นไฟล์ไบนารี .eim"
      ],
      "correct_index": 1,
      "correct_letter": "ข",
      "explanation": "App.run() ทำหน้าที่เริ่มต้น Event Loop หลักของระบบเพื่อสั่งให้ทุกมอดูล Brick เริ่มต้นทำงานและรับส่งข้อมูลระหว่างกัน",
      "points": 1
    },
    {
      "id": "q_ch02_03",
      "quiz_uid": 13,
      "chapter_id": "ch02",
      "category": "chapter_quiz",
      "chapter_number": 2,
      "question_type": "multiple_choice",
      "question_text": "การทำงานร่วมกันระหว่างหน่วยประมวลผล MPU และ MCU บนบอร์ด Arduino UNO Q มีการแบ่งหน้าที่หลักตามข้อใด",
      "options": [
        "MPU ประมวลผลโมเดล AI และรันระบบปฏิบัติการลีนุกซ์ ส่วน MCU จัดการสัญญาณควบคุมฮาร์ดแวร์แบบเวลาจริง",
        "MCU รันระบบปฏิบัติการลีนุกซ์ ส่วน MPU มีหน้าที่จ่ายไฟให้หลอดไฟ LED",
        "ทั้งสองหน่วยสลับกันทำงานทุก ๆ 1 นาทีตามการตั้งค่าเวลา",
        "MPU มีหน้าที่เชื่อมต่อ Wi-Fi อย่างเดียว ส่วนงานอื่น ๆ ทั้งหมดจัดการโดย MCU"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "สถาปัตยกรรม Heterogeneous บน UNO Q ใช้ MPU (Linux AArch64) รันระบบและโมเดล AI หนัก ๆ ส่วน MCU จัดการ I/O ตอบสนองฮาร์ดแวร์แบบเรียลไทม์",
      "points": 1
    },
    {
      "id": "q_ch02_04",
      "quiz_uid": 14,
      "chapter_id": "ch02",
      "category": "chapter_quiz",
      "chapter_number": 2,
      "question_type": "multiple_choice",
      "question_text": "การควบคุมหลอดไฟ LED Matrix บนบอร์ด Arduino UNO Q มีประโยชน์หลักตามข้อใดในการพัฒนาแอปพลิเคชัน Edge AI",
      "options": [
        "ช่วยเพิ่มความเร็วในการประมวลผลของโมเดลปัญญาประดิษฐ์",
        "แสดงผลภาพเคลื่อนไหวและไอคอนสัญลักษณ์เพื่อแจ้งเตือนสถานะของระบบให้ผู้ใช้ทราบทันที",
        "ทำหน้าที่เป็นเลนส์เสริมสำหรับการจับภาพของกล้องดิจิทัล",
        "ทำหน้าที่ระบายความร้อนให้แก่ชิปประมวลผลหลัก"
      ],
      "correct_index": 1,
      "correct_letter": "ข",
      "explanation": "LED Matrix บนบอร์ดถูกใช้แสดงผลสัญลักษณ์ กราฟิก หรือไอคอนแจ้งสถานะ เช่น พร้อมทำงาน ตรวจพบข้อผิดพลาด หรือผลการจำแนก",
      "points": 1
    },
    {
      "id": "q_ch02_05",
      "quiz_uid": 15,
      "chapter_id": "ch02",
      "category": "chapter_quiz",
      "chapter_number": 2,
      "question_type": "multiple_choice",
      "question_text": "ในการเขียนโปรแกรมรับค่าจากปุ่มกดบนบอร์ด Arduino UNO Q นิยมใช้กลไกแบบใดเพื่อตอบสนองต่อการกดปุ่มได้อย่างมีประสิทธิภาพ",
      "options": [
        "การเขียนคำสั่งวนลูปตรวจสอบตลอดเวลาโดยไม่มีการพักการทำงาน (Busy Waiting)",
        "การใช้ฟังก์ชัน Callback หรือการดักจับเหตุการณ์ (Event-Driven Listener)",
        "การปิดระบบปฏิบัติการลีนุกซ์แล้วรอสัญญาณเปิดใหม่",
        "การส่งข้อมูลผ่านเครือข่ายอินเทอร์เน็ตไปถามเซิร์ฟเวอร์ภายนอก"
      ],
      "correct_index": 1,
      "correct_letter": "ข",
      "explanation": "การดักจับเหตุการณ์แบบ Event Callback ทำให้ซีพียูไม่ต้องเสียเวลาตรวจสอบสถานะปุ่มตลอดเวลา ช่วยประหยัดทรัพยากรและตอบสนองได้ทันที",
      "points": 1
    },
    {
      "id": "q_ch02_06",
      "quiz_uid": 16,
      "chapter_id": "ch02",
      "category": "chapter_quiz",
      "chapter_number": 2,
      "question_type": "multiple_choice",
      "question_text": "ฟังก์ชันใดที่ใช้สำหรับการแสดงข้อความบันทึกการทำงาน (Log Output) บนหน้าต่าง Console เพื่อช่วยตรวจสอบสถานะของ Brick",
      "options": [
        "print() หรือระบบ Logging ประจำ Brick",
        "format_disk()",
        "reboot_system()",
        "connect_wifi()"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "คำสั่งแสดงผลข้อความมาตรฐานหรือเมธอด Logging ของ Brick ใช้ส่งข้อความตรวจเช็กสถานะการทำงาน (Debugging/Monitoring) ออกมายังคอนโซล",
      "points": 1
    },
    {
      "id": "q_ch02_07",
      "quiz_uid": 17,
      "chapter_id": "ch02",
      "category": "chapter_quiz",
      "chapter_number": 2,
      "question_type": "multiple_choice",
      "question_text": "ข้อใดคือประโยชน์สำคัญของการส่งผ่านข้อความเหตุการณ์ระหว่างมอดูล (Message / Event Broker)",
      "options": [
        "ทำให้แต่ละมอดูลไม่ต้องขึ้นต่อกันโดยตรง (Decoupling) เพิ่มความยืดหยุ่นในการปรับเปลี่ยนระบบ",
        "ทำให้ขนาดของไฟล์โปรแกรมมีขนาดใหญ่ขึ้นเพื่อความปลอดภัย",
        "ช่วยเพิ่มความเร็วอินเทอร์เน็ตในห้องปฏิบัติการ",
        "บังคับให้โมเดลปัญญาประดิษฐ์ทำงานได้เพียงโมเดลเดียว"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "กลไก Message/Event Broker ช่วยให้มอดูลแยกตัวเป็นอิสระ (Decoupling) เมื่อต้องการเพิ่มหรือถอดมอดูลใดออกก็ไม่กระทบกับส่วนอื่น",
      "points": 1
    },
    {
      "id": "q_ch02_08",
      "quiz_uid": 18,
      "chapter_id": "ch02",
      "category": "chapter_quiz",
      "chapter_number": 2,
      "question_type": "multiple_choice",
      "question_text": "ในสคริปต์ภาษาไพทอน brick_runner.py การสร้างอินสแตนซ์ของ Brick และนำมาลงทะเบียนมีวัตถุประสงค์เพื่ออะไร",
      "options": [
        "เพื่อกำหนดค่าเริ่มต้นและเชื่อมโยงมอดูลต่าง ๆ เข้ากับวงจรการทำงานหลักของระบบ",
        "เพื่อลบไดรเวอร์ทั้งหมดที่ติดตั้งอยู่บนบอร์ด",
        "เพื่อแปลงไฟล์ภาพถ่ายให้เป็นไฟล์เสียง",
        "เพื่อสั่งหยุดการจ่ายกระแสไฟไปยังพอร์ต USB"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "สคริปต์ brick_runner.py ทำหน้าที่สร้างและผูกโยงมอดูลต่าง ๆ เข้าด้วยกัน พร้อมรันแอปพลิเคชันอย่างเป็นระบบ",
      "points": 1
    },
    {
      "id": "q_ch02_09",
      "quiz_uid": 19,
      "chapter_id": "ch02",
      "category": "chapter_quiz",
      "chapter_number": 2,
      "question_type": "multiple_choice",
      "question_text": "ข้อใดคือข้อได้เปรียบหลักของการเขียนโปรแกรมแบบแยกมอดูล (Modular Architecture) เมื่อเทียบกับการเขียนโค้ดรวมเป็นไฟล์เดียว",
      "options": [
        "ง่ายต่อการทดสอบ ค้นหาจุดผิดพลาด และนำมอดูลเดิมไปประยุกต์ใช้ซ้ำในโครงงานอื่น",
        "ทำให้คอมพิวเตอร์ใช้หน่วยความจำแรมจนเต็มประสิทธิภาพ",
        "ไม่ต้องมีขั้นตอนการคอมไพล์โค้ดในทุกกรณี",
        "จำกัดไม่ให้บุคคลอื่นสามารถอ่านโค้ดโปรแกรมได้"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "สถาปัตยกรรมแบบมอดูลช่วยให้ดูแลรักษาโค้ดง่าย ทดสอบทีละส่วนได้ชัดเจน และนำบล็อกฟังก์ชันไปต่อยอดในงานอื่นได้ทันที",
      "points": 1
    },
    {
      "id": "q_ch02_10",
      "quiz_uid": 20,
      "chapter_id": "ch02",
      "category": "chapter_quiz",
      "chapter_number": 2,
      "question_type": "multiple_choice",
      "question_text": "เมื่อต้องการยกเลิกการทำงานของระบบหรือปิดแอปพลิเคชันอย่างถูกต้อง ข้อใดคือแนวปฏิบัติที่ดีในการจัดการทรัพยากร",
      "options": [
        "ดึงสายไฟเลี้ยงออกจากบอร์ดทันทีขณะที่ระบบกำลังประมวลผล",
        "ดักจับสัญญาณยกเลิก (เช่น KeyboardInterrupt) แล้วสั่งปิดการเชื่อมต่อและคืนทรัพยากรฮาร์ดแวร์ (Cleanup)",
        "สั่งให้โปรแกรมวนลูปทำงานต่อไปเรื่อย ๆ จนกว่าหน่วยความจำจะเต็ม",
        "ลบสคริปต์ภาษาไพทอนทิ้งทั้งหมด"
      ],
      "correct_index": 1,
      "correct_letter": "ข",
      "explanation": "การดักจับสัญญาณหยุดการทำงานเพื่อทำ Cleanup และปิดการเชื่อมต่ออุปกรณ์ต่าง ๆ อย่างถูกต้อง ช่วยป้องกันความเสียหายต่อฮาร์ดแวร์และข้อมูลในระบบ",
      "points": 1
    }
  ],

  3: [
    {
      "id": "q_ch03_01",
      "quiz_uid": 21,
      "chapter_id": "ch03",
      "category": "chapter_quiz",
      "chapter_number": 3,
      "question_type": "multiple_choice",
      "question_text": "มอดูล Database-SQL Brick บนบอร์ดพัฒนา Arduino UNO Q ใช้ระบบจัดการฐานข้อมูล (DBMS) ชนิดใดในการทำงานบนระบบปฏิบัติการลีนุกซ์",
      "options": [
        "Oracle Database Enterprise",
        "SQLite (ระบบจัดการฐานข้อมูลเชิงสัมพันธ์แบบฝังตัว)",
        "Microsoft Access 97",
        "Apache Cassandra NoSQL"
      ],
      "correct_index": 1,
      "correct_letter": "ข",
      "explanation": "Database-SQL Brick ใช้ SQLite ซึ่งเป็น Relational Database ขนาดเล็ก น้ำหนักเบา ไม่ต้องติดตั้ง Server เหมาะกับระบบสมองกลฝังตัว",
      "points": 1
    },
    {
      "id": "q_ch03_02",
      "quiz_uid": 22,
      "chapter_id": "ch03",
      "category": "chapter_quiz",
      "chapter_number": 3,
      "question_type": "multiple_choice",
      "question_text": "เหตุใดการจัดเก็บบันทึกประวัติการตรวจจับของโมเดล AI (Inference Event Logging) ลงในฐานข้อมูลบนตัวบอร์ดโดยตรง จึงมีความสำคัญในงาน Edge AI",
      "options": [
        "เพื่อบันทึกประวัติการตัดสินใจย้อนหลังได้แบบออฟไลน์โดยไม่ต้องพึ่งพาเซิร์ฟเวอร์ภายนอกตลอดเวลา",
        "เพื่อช่วยเพิ่มความละเอียดพิกเซลของภาพถ่ายจากกล้อง",
        "เพื่อลดความร้อนของชิปหน่วยประมวลผลกลาง",
        "เพื่อป้องกันไม่ให้ผู้ใช้อื่นเข้าถึงโค้ดภาษาไพทอน"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "การเก็บบันทึกบนบอร์ดโดยตรงช่วยให้ระบบบันทึกประวัติผลการทำงานได้อย่างต่อเนื่องแม้ไม่มีสัญญาณเครือข่าย และเรียกดูย้อนหลังได้ทันที",
      "points": 1
    },
    {
      "id": "q_ch03_03",
      "quiz_uid": 23,
      "chapter_id": "ch03",
      "category": "chapter_quiz",
      "chapter_number": 3,
      "question_type": "multiple_choice",
      "question_text": "หากต้องการสร้างตารางข้อมูลใหม่ชื่อ detection_logs เพื่อบันทึกผลการตรวจจับ ต้องใช้คำสั่งภาษา SQL ในข้อใด",
      "options": [
        "NEW TABLE detection_logs (...)",
        "CREATE TABLE detection_logs (...)",
        "MAKE TABLE detection_logs (...)",
        "BUILD TABLE detection_logs (...)"
      ],
      "correct_index": 1,
      "correct_letter": "ข",
      "explanation": "คำสั่งมาตรฐานในภาษา SQL สำหรับสร้างตารางใหม่คือ CREATE TABLE ตามด้วยชื่อตารางและโครงสร้างคอลัมน์",
      "points": 1
    },
    {
      "id": "q_ch03_04",
      "quiz_uid": 24,
      "chapter_id": "ch03",
      "category": "chapter_quiz",
      "chapter_number": 3,
      "question_type": "multiple_choice",
      "question_text": "ชนิดข้อมูล (Data Type) ในภาษา SQL ข้อใดเหมาะสมที่สุดสำหรับการจัดเก็บค่าคะแนนความเชื่อมั่น (Confidence Score) เช่น 0.945",
      "options": [
        "TEXT",
        "BOOLEAN",
        "REAL หรือ FLOAT (จำนวนจริงทศนิยม)",
        "BLOB"
      ],
      "correct_index": 2,
      "correct_letter": "ค",
      "explanation": "ค่าทศนิยมของคะแนนความเชื่อมั่น เช่น 0.945 ต้องจัดเก็บด้วยชนิดข้อมูล REAL หรือ FLOAT เพื่อให้สามารถนำไปคำนวณทางคณิตศาสตร์ต่อได้",
      "points": 1
    },
    {
      "id": "q_ch03_05",
      "quiz_uid": 25,
      "chapter_id": "ch03",
      "category": "chapter_quiz",
      "chapter_number": 3,
      "question_type": "multiple_choice",
      "question_text": "คำสั่งภาษา SQL ข้อใดใช้สำหรับเพิ่มข้อมูลแถวใหม่ (Record) ลงในตารางฐานข้อมูลเมื่อโมเดลทำนายผลเสร็จสิ้น",
      "options": [
        "INSERT INTO detection_logs VALUES (...)",
        "UPDATE detection_logs SET (...)",
        "ADD ROW detection_logs (...)",
        "PUSH TO detection_logs (...)"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "คำสั่ง INSERT INTO ใช้สำหรับเพิ่มระเบียนหรือแถวข้อมูลใหม่เข้าสู่ตารางในฐานข้อมูลเชิงสัมพันธ์",
      "points": 1
    },
    {
      "id": "q_ch03_06",
      "quiz_uid": 26,
      "chapter_id": "ch03",
      "category": "chapter_quiz",
      "chapter_number": 3,
      "question_type": "multiple_choice",
      "question_text": "หากต้องการสืบค้นเฉพาะรายการที่มีผลการตรวจจับเป็นชิ้นงานเสีย (status = 'NG') ควรเขียนคำสั่งตามข้อใด",
      "options": [
        "SELECT * FROM detection_logs WHERE status = 'NG';",
        "FIND * FROM detection_logs IF status = 'NG';",
        "GET * FROM detection_logs MATCH 'NG';",
        "SEARCH detection_logs FOR status == 'NG';"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "ไวยากรณ์ SQL มาตรฐานในการสืบค้นข้อมูลตามเงื่อนไขคือการใช้คำสั่ง SELECT ร่วมกับคำสั่ง WHERE เพื่อกรองข้อมูลที่ตรงตามเกณฑ์",
      "points": 1
    },
    {
      "id": "q_ch03_07",
      "quiz_uid": 27,
      "chapter_id": "ch03",
      "category": "chapter_quiz",
      "chapter_number": 3,
      "question_type": "multiple_choice",
      "question_text": "คำสั่งภาษา SQL ข้อใดใช้สำหรับนับจำนวนชิ้นงานทั้งหมด โดยจัดกลุ่มแยกตามประเภทของชิ้นงาน (label)",
      "options": [
        "SELECT label, COUNT(*) FROM detection_logs GROUP BY label;",
        "SELECT label, SUM(*) FROM detection_logs ORDER BY label;",
        "COUNT ALL FROM detection_logs SEPARATE BY label;",
        "CALCULATE TOTAL FROM detection_logs DIVIDE label;"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "การสรุปจำนวนแยกกลุ่มใน SQL ใช้ฟังก์ชัน COUNT(*) ควบคู่กับประโยค GROUP BY ตามชื่อคอลัมน์ที่ต้องการจัดกลุ่ม",
      "points": 1
    },
    {
      "id": "q_ch03_08",
      "quiz_uid": 28,
      "chapter_id": "ch03",
      "category": "chapter_quiz",
      "chapter_number": 3,
      "question_type": "multiple_choice",
      "question_text": "ในโปรแกรมภาษาไพทอน db_logger.py เหตุใดหลังจากเรียกคำสั่ง cursor.execute(INSERT ...) จึงต้องเรียกคำสั่ง conn.commit() เสมอ",
      "options": [
        "เพื่อปิดหน้าต่างโปรแกรมลงทันที",
        "เพื่อยืนยันและบันทึกการเปลี่ยนแปลงข้อมูลลงสู่ไฟล์ฐานข้อมูลอย่างถาวร",
        "เพื่อรีเซ็ตหมายเลข IP ของบอร์ดพัฒนา",
        "เพื่อลบข้อมูลในหน่วยความจำแคชทิ้งทั้งหมด"
      ],
      "correct_index": 1,
      "correct_letter": "ข",
      "explanation": "คำสั่ง commit() เป็นการยืนยัน Transaction เพื่อบันทึกข้อมูลที่เพิ่มหรือแก้ไขลงในไฟล์ฐานข้อมูลจริงอย่างสมบูรณ์",
      "points": 1
    },
    {
      "id": "q_ch03_09",
      "quiz_uid": 29,
      "chapter_id": "ch03",
      "category": "chapter_quiz",
      "chapter_number": 3,
      "question_type": "multiple_choice",
      "question_text": "คอลัมน์ข้อมูลข้อใดมีความจำเป็นอย่างยิ่งสำหรับการจัดเก็บในตารางบันทึกผล เพื่อใช้จัดเรียงลำดับเหตุการณ์ตามเวลาที่เกิดขึ้นจริง",
      "options": [
        "timestamp หรือ created_at (วันและเวลาที่ตรวจจับ)",
        "cpu_serial_number",
        "wifi_password",
        "board_color"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "การบันทึก Timestamp (วันและเวลา) ทำให้ทราบว่าเหตุการณ์หรือผลการตรวจจับนั้นเกิดขึ้นเมื่อใด และสามารถนำไปเรียงลำดับหรือจัดทำรายงานย้อนหลังได้",
      "points": 1
    },
    {
      "id": "q_ch03_10",
      "quiz_uid": 30,
      "chapter_id": "ch03",
      "category": "chapter_quiz",
      "chapter_number": 3,
      "question_type": "multiple_choice",
      "question_text": "การนำข้อมูลสถิติที่บันทึกใน Database-SQL Brick ไปใช้วิเคราะห์ย้อนหลัง มีประโยชน์โดยตรงต่อระบบอุตสาหกรรมในด้านใด",
      "options": [
        "การประเมินอัตราของเสียและสนับสนุนการบำรุงรักษาเชิงคาดการณ์ (Predictive Maintenance)",
        "การลดความเร็วของเครื่องจักรลงครึ่งหนึ่งเพื่อประหยัดไฟ",
        "การเปลี่ยนชนิดของวัสดุที่ใช้ผลิตบอร์ดสมองกล",
        "การยกเลิกการใช้กล้องตรวจจับในสายการผลิต"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "ข้อมูลสถิติการตรวจจับที่บันทึกอย่างต่อเนื่องสามารถนำมาคำนวณอัตราความผิดปกติ วางแผนซ่อมบำรุงเครื่องจักรล่วงหน้า และพัฒนาคุณภาพการผลิต",
      "points": 1
    }
  ],

  4: [
    {
      "id": "q_ch04_01",
      "quiz_uid": 31,
      "chapter_id": "ch04",
      "category": "chapter_quiz",
      "chapter_number": 4,
      "question_type": "multiple_choice",
      "question_text": "ในขั้นตอนการเริ่มต้นโครงการปัญญาประดิษฐ์บนแพลตฟอร์ม Edge Impulse Studio ขั้นตอนแรกสุดหลังจากสร้างโปรเจกต์คือข้อใด",
      "options": [
        "การดาวน์โหลดไฟล์ .eim ไปติดตั้งบนบอร์ดทันที",
        "การรวบรวมและนำเข้าชุดข้อมูลตัวอย่างเข้าสู่ระบบ (Data Acquisition)",
        "การเขียนโค้ดภาษาไพทอนเพื่อควบคุมเซอร์โวมอเตอร์",
        "การซื้ออุปกรณ์ฮาร์ดแวร์เพิ่มเติมจากทางเว็บไซต์"
      ],
      "correct_index": 1,
      "correct_letter": "ข",
      "explanation": "กระบวนการพัฒนาปัญญาประดิษฐ์ต้องเริ่มต้นจากการรวบรวมและนำเข้าชุดข้อมูลตัวอย่าง (Data Acquisition) ก่อนเป็นลำดับแรกสุดเสมอ",
      "points": 1
    },
    {
      "id": "q_ch04_02",
      "quiz_uid": 32,
      "chapter_id": "ch04",
      "category": "chapter_quiz",
      "chapter_number": 4,
      "question_type": "multiple_choice",
      "question_text": "เมนูใดบนแถบเครื่องมือด้านซ้ายของ Edge Impulse Studio ที่ใช้สำหรับนำเข้าและบริหารจัดการชุดข้อมูลภาพ",
      "options": [
        "Dashboard",
        "Data acquisition",
        "Deployment",
        "Versioning"
      ],
      "correct_index": 1,
      "correct_letter": "ข",
      "explanation": "เมนู Data acquisition คือส่วนจัดการนำเข้าข้อมูล ทั้งการอัปโหลดไฟล์ การเชื่อมต่อกล้อง และการกำหนดป้ายกำกับข้อมูล",
      "points": 1
    },
    {
      "id": "q_ch04_03",
      "quiz_uid": 33,
      "chapter_id": "ch04",
      "category": "chapter_quiz",
      "chapter_number": 4,
      "question_type": "multiple_choice",
      "question_text": "การจัดสรรสัดส่วนชุดข้อมูลฝึกสอน (Training Set) ต่อชุดข้อมูลทดสอบ (Testing Set) ในอัตราส่วนมาตรฐาน 80:20 มีวัตถุประสงค์เพื่ออะไร",
      "options": [
        "เพื่อแบ่งข้อมูลส่วนใหญ่ให้โมเดลใช้เรียนรู้ และกันข้อมูลอีกส่วนไว้ประเมินความแม่นยำอย่างเป็นกลาง",
        "เพื่อให้ไฟล์โมเดลมีขนาดเล็กลงร้อยละ 20",
        "เพื่อเพิ่มความเร็วในการอัปโหลดภาพขึ้นสู่คลาวด์",
        "เพื่อป้องกันไม่ให้ผู้อื่นมองเห็นชุดข้อมูลภาพของเรา"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "สัดส่วน 80:20 เป็นเกณฑ์มาตรฐานที่ทำให้โมเดลมีข้อมูลเรียนรู้เพียงพอ และมีชุดข้อมูลทดสอบที่โมเดลไม่เคยเห็นไว้ใช้วัดผลจริงได้อย่างน่าเชื่อถือ",
      "points": 1
    },
    {
      "id": "q_ch04_04",
      "quiz_uid": 34,
      "chapter_id": "ch04",
      "category": "chapter_quiz",
      "chapter_number": 4,
      "question_type": "multiple_choice",
      "question_text": "เหตุใดในการเก็บรวบรวมภาพตัวอย่างของชิ้นงาน จึงต้องถ่ายภาพในสภาวะที่มีแสง มุมมอง และระยะห่างที่หลากหลาย",
      "options": [
        "เพื่อให้โมเดลมีความทนทาน (Robustness) และสามารถทำนายผลได้ถูกต้องในสภาพแวดล้อมการทำงานจริง",
        "เพื่อให้ไฟล์ภาพมีความสวยงามและมีสีสันสดใสมากขึ้น",
        "เพื่อลดจำนวนภาพที่ต้องอัปโหลดเข้าสู่ระบบ",
        "เพื่อหลีกเลี่ยงการใช้พื้นที่จัดเก็บบนระบบคลาวด์"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "การเก็บข้อมูลที่มีความหลากหลายของสภาพแสง มุมกล้อง และฉากหลัง ช่วยป้องกันไม่ให้โมเดลยึดติดกับสภาพแวดล้อมเดิม และทำงานได้แม่นยำในหน้างานจริง",
      "points": 1
    },
    {
      "id": "q_ch04_05",
      "quiz_uid": 35,
      "chapter_id": "ch04",
      "category": "chapter_quiz",
      "chapter_number": 4,
      "question_type": "multiple_choice",
      "question_text": "หากต้องการฝึกสอนโมเดลสำหรับงานที่ต้องตีกรอบสี่เหลี่ยมระบุตำแหน่งของวัตถุ ต้องเลือกรูปแบบการติดป้ายกำกับ (Labeling Method) ในข้อใด",
      "options": [
        "One label per data item",
        "Bounding boxes (object detection)",
        "Time-series classification",
        "Multi-label regression"
      ],
      "correct_index": 1,
      "correct_letter": "ข",
      "explanation": "โหมด Bounding boxes ใช้สำหรับงานตรวจจับวัตถุที่ต้องการระบุทั้งชนิดและพิกัดตำแหน่งกรอบของวัตถุในภาพ",
      "points": 1
    },
    {
      "id": "q_ch04_06",
      "quiz_uid": 36,
      "chapter_id": "ch04",
      "category": "chapter_quiz",
      "chapter_number": 4,
      "question_type": "multiple_choice",
      "question_text": "ฟังก์ชัน \"Train / Test Split\" บนแพลตฟอร์ม Edge Impulse ช่วยอำนวยความสะดวกให้แก่ผู้พัฒนาในเรื่องใด",
      "options": [
        "การสุ่มกระจายข้อมูลระหว่างชุดฝึกสอนและชุดทดสอบให้ได้สัดส่วนที่สมดุลโดยอัตโนมัติ",
        "การตัดต่อภาพวิดีโอให้เป็นภาพนิ่ง",
        "การลบภาพที่มีคุณภาพต่ำออกจากโครงการโดยไม่ต้องตรวจสอบ",
        "การส่งโมเดลไปยังอุปกรณ์ปลายทางผ่านระบบคลาวด์"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "ฟังก์ชัน Train/Test Split จะช่วยสุ่มแบ่งข้อมูลในแต่ละคลาสให้ได้สัดส่วนที่เหมาะสม (เช่น 80:20) อย่างทั่วถึงและรวดเร็ว",
      "points": 1
    },
    {
      "id": "q_ch04_07",
      "quiz_uid": 37,
      "chapter_id": "ch04",
      "category": "chapter_quiz",
      "chapter_number": 4,
      "question_type": "multiple_choice",
      "question_text": "ภาวะที่ชุดข้อมูลมีจำนวนภาพของคลาสหนึ่งมากเกินไป แต่มีภาพของอีกคลาสหนึ่งน้อยมาก เรียกว่าอะไร และส่งผลเสียอย่างไร",
      "options": [
        "Overclocking ทำให้คอมพิวเตอร์เกิดความร้อนสูง",
        "Class Imbalance ทำให้โมเดลมีแนวโน้มที่จะทำนายเอนเอียงไปยังคลาสที่มีข้อมูลมากกว่า",
        "Data Encryption ทำให้ไม่สามารถอ่านข้อมูลภาพได้",
        "Buffer Overflow ทำให้ระบบปฏิบัติการหยุดทำงาน"
      ],
      "correct_index": 1,
      "correct_letter": "ข",
      "explanation": "Class Imbalance (ความไม่สมดุลของข้อมูล) จะทำให้โมเดลเอนเอียง (Bias) ไปทายคลาสที่มีข้อมูลเยอะเป็นหลัก และไม่สามารถจำแนกคลาสที่มีข้อมูลน้อยได้ดี",
      "points": 1
    },
    {
      "id": "q_ch04_08",
      "quiz_uid": 38,
      "chapter_id": "ch04",
      "category": "chapter_quiz",
      "chapter_number": 4,
      "question_type": "multiple_choice",
      "question_text": "ในหน้า Impulse Design ส่วนของ Input Block มีหน้าที่กำหนดค่าพารามิเตอร์ใดของข้อมูลภาพ",
      "options": [
        "ขนาดความกว้างและความสูงของภาพ (Image width & height) และโหมดสี (RGB/Grayscale)",
        "ชนิดของเลนส์กล้องที่ติดตั้งบนคอมพิวเตอร์",
        "จำนวนรอบในการฝึกสอนโครงข่ายประสาทเทียม (Epochs)",
        "ความเร็วในการหมุนของสายพานลำเลียง"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "Input Block ใน Impulse Design กำหนดมิติขนาดพิกเซลของภาพ (เช่น 96x96 หรือ 160x160) และระบบสีที่จะป้อนเข้าสู่โมเดล",
      "points": 1
    },
    {
      "id": "q_ch04_09",
      "quiz_uid": 39,
      "chapter_id": "ch04",
      "category": "chapter_quiz",
      "chapter_number": 4,
      "question_type": "multiple_choice",
      "question_text": "หากผู้พัฒนากำหนดขนาดมิติภาพใน Input Block ให้มีขนาดใหญ่มากเกินไป จะส่งผลกระทบต่อบอร์ดสมองกลฝังตัวอย่างไร",
      "options": [
        "ทำให้โมเดลประมวลผลช้าลง ใช้หน่วยความจำแรมสูงขึ้น และเกิดความหน่วง (High Latency)",
        "ทำให้บอร์ดพัฒนาไม่สามารถเชื่อมต่อสัญญาณ Wi-Fi ได้",
        "ทำให้ภาพถ่ายที่บันทึกมีความคมชัดต่ำลง",
        "ทำให้ไม่สามารถเขียนโค้ดภาษาไพทอนได้"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "ภาพขนาดใหญ่ต้องใช้การคำนวณและหน่วยความจำมหาศาล ส่งผลให้โมเดลรันช้าลง เกิดความหน่วงสูง และอาจทำให้แรมของระบบฝังตัวไม่เพียงพอ",
      "points": 1
    },
    {
      "id": "q_ch04_10",
      "quiz_uid": 40,
      "chapter_id": "ch04",
      "category": "chapter_quiz",
      "chapter_number": 4,
      "question_type": "multiple_choice",
      "question_text": "สคริปต์ data_pipeline_check.py ถูกพัฒนาขึ้นเพื่อทำหน้าที่ตรวจสอบความพร้อมของระบบในด้านใด",
      "options": [
        "ตรวจสอบความถูกต้องของสัดส่วนชุดข้อมูล จำนวนไฟล์ภาพ และความสมบูรณ์ของไปป์ไลน์ข้อมูล",
        "ตรวจสอบระดับแบตเตอรี่ของสมาร์ทโฟน",
        "ตรวจสอบรหัสผ่านของระบบปฏิบัติการวินโดวส์",
        "ตรวจสอบราคาของอุปกรณ์บนอินเทอร์เน็ต"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "สคริปต์ data_pipeline_check.py ใช้สำหรับตรวจสอบความถูกต้องของโครงสร้างชุดข้อมูล ความสมดุลของคลาส และความพร้อมก่อนเริ่มการฝึกสอนโมเดล",
      "points": 1
    }
  ],

  5: [
    {
      "id": "q_ch05_01",
      "quiz_uid": 41,
      "chapter_id": "ch05",
      "category": "chapter_quiz",
      "chapter_number": 5,
      "question_type": "multiple_choice",
      "question_text": "หลักการจำแนกประเภทข้อมูลแบบกลุ่มเดียว (One-Class Classification) ในงาน Visual Anomaly Detection มีลักษณะการทำงานอย่างไร",
      "options": [
        "โมเดลจะเรียนรู้เฉพาะลักษณะของชิ้นงานปกติ และถือว่าสิ่งใดที่มีคุณลักษณะแปลกแยกออกไปคือความผิดปกติ",
        "โมเดลต้องเรียนรู้ตัวอย่างชิ้นงานเสียทุกรูปแบบที่มีอยู่ในโลก",
        "โมเดลจะสุ่มทายผลลัพธ์โดยไม่ต้องอาศัยข้อมูลตัวอย่าง",
        "โมเดลจะแปลงภาพชิ้นงานให้เป็นข้อความบรรยายลักษณะชิ้นงาน"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "One-Class Classification อาศัยการสร้างขอบเขตของคุณลักษณะชิ้นงานปกติ (Good) เมื่อมีภาพชิ้นงานใดตกอยู่นอกขอบเขต ระบบจะถือว่าเป็นความผิดปกติ (Anomaly)",
      "points": 1
    },
    {
      "id": "q_ch05_02",
      "quiz_uid": 42,
      "chapter_id": "ch05",
      "category": "chapter_quiz",
      "chapter_number": 5,
      "question_type": "multiple_choice",
      "question_text": "เหตุใดในสายการผลิตทางอุตสาหกรรม การฝึกสอนโมเดล Visual Anomaly Detection จึงนิยมใช้เฉพาะข้อมูลของ \"ชิ้นงานปกติ\"",
      "options": [
        "เพราะในความเป็นจริง ของเสียเกิดขึ้นน้อยมากและมีรูปแบบความเสียหายที่หลากหลายจนไม่สามารถเก็บตัวอย่างได้ครบถ้วน",
        "เพราะชิ้นงานเสียมีราคาแพงกว่าชิ้นงานปกติ",
        "เพราะระบบปฏิบัติการลีนุกซ์ไม่อนุญาตให้อัปโหลดภาพของเสีย",
        "เพราะภาพของเสียจะทำให้กล้องดิจิทัลชำรุดเสียหาย"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "ในโรงงาน ชิ้นงานเสียเกิดขึ้นได้หลายรูปแบบ (รอยแตก รอยไหม้ สีเพี้ยน ชิ้นส่วนขาด) จึงเป็นไปไม่ได้ที่จะเก็บตัวอย่างของเสียได้ครบทุกชนิด การฝึกเฉพาะของปกติจึงตอบโจทย์ที่สุด",
      "points": 1
    },
    {
      "id": "q_ch05_03",
      "quiz_uid": 43,
      "chapter_id": "ch05",
      "category": "chapter_quiz",
      "chapter_number": 5,
      "question_type": "multiple_choice",
      "question_text": "สถาปัตยกรรมโมเดลตรวจจับความผิดปกติที่ได้รับการออกแบบให้มีขนาดกะทัดรัดและประมวลผลได้รวดเร็วบน Edge Impulse คือสถาปัตยกรรมใด",
      "options": [
        "ResNet-152 Deep Residual Network",
        "FOMO-AD (Faster Objects, More Objects - Anomaly Detection)",
        "VGG-19 Large Architecture",
        "BERT Transformer Architecture"
      ],
      "correct_index": 1,
      "correct_letter": "ข",
      "explanation": "FOMO-AD เป็นสถาปัตยกรรมตรวจจับความผิดปกติที่พัฒนาขึ้นเป็นพิเศษสำหรับอุปกรณ์ขอบข่ายขนาดเล็ก ใช้หน่วยความจำน้อยและประมวลผลได้เร็วมาก",
      "points": 1
    },
    {
      "id": "q_ch05_04",
      "quiz_uid": 44,
      "chapter_id": "ch05",
      "category": "chapter_quiz",
      "chapter_number": 5,
      "question_type": "multiple_choice",
      "question_text": "ในหน้าต่าง Impulse Design สำหรับงาน Visual Anomaly Detection บล็อกการเรียนรู้ (Learning Block) ที่ต้องเลือกใช้คือข้อใด",
      "options": [
        "Visual Anomaly Detection (FOMO-AD)",
        "K-Means Clustering Only",
        "Linear Regression Block",
        "Audio Synthesizer Block"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "การพัฒนาโมเดลตรวจจับความผิดปกติจากภาพบน Edge Impulse ต้องเลือก Learning Block เป็น Visual Anomaly Detection (FOMO-AD)",
      "points": 1
    },
    {
      "id": "q_ch05_05",
      "quiz_uid": 45,
      "chapter_id": "ch05",
      "category": "chapter_quiz",
      "chapter_number": 5,
      "question_type": "multiple_choice",
      "question_text": "เครื่องมือ \"Feature Explorer\" บนหน้าการฝึกสอนของ Edge Impulse ช่วยให้ผู้พัฒนาสามารถสังเกตสิ่งใดได้อย่างชัดเจน",
      "options": [
        "การกระจายตัวของเวกเตอร์คุณลักษณะ และการเกาะกลุ่มของข้อมูลปกติเทียบกับจุดที่ผิดปกติ",
        "อุณหภูมิความร้อนของชิปซีพียูขณะกำลังฝึกสอน",
        "อัตราการไหลของกระแสไฟฟ้าในสายเคเบิล USB",
        "ความเร็วของพัดลมระบายความร้อนบนเครื่องแม่ข่าย"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "Feature Explorer แสดงภาพการกระจายตัวของข้อมูลในมิติคุณลักษณะ ช่วยให้เห็นว่าข้อมูลชิ้นงานปกติเกาะกลุ่มกันดีหรือไม่ และมีข้อมูลใดหลุดกลุ่มแปลกแยกออกไป",
      "points": 1
    },
    {
      "id": "q_ch05_06",
      "quiz_uid": 46,
      "chapter_id": "ch05",
      "category": "chapter_quiz",
      "chapter_number": 5,
      "question_type": "multiple_choice",
      "question_text": "ค่า \"Anomaly Max Score\" ที่โมเดลคำนวณออกมาในการตรวจสอบภาพ มีความหมายตรงกับข้อใด",
      "options": [
        "ระดับคะแนนความผิดปกติสูงสุดที่ตรวจพบในพื้นที่ย่อยของภาพ",
        "จำนวนชิ้นงานทั้งหมดที่ผลิตได้ในโรงงาน",
        "เปอร์เซ็นต์ความจุของหน่วยความจำแรมที่เหลืออยู่",
        "ความสว่างเฉลี่ยของหลอดไฟในห้องทดลอง"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "Anomaly Max Score คือค่าคะแนนความผิดปกติของจุดหรือกรอบพื้นที่ย่อยที่มีค่าความเบี่ยงเบนสูงที่สุดในภาพนั้น",
      "points": 1
    },
    {
      "id": "q_ch05_07",
      "quiz_uid": 47,
      "chapter_id": "ch05",
      "category": "chapter_quiz",
      "chapter_number": 5,
      "question_type": "multiple_choice",
      "question_text": "การกำหนดค่าเกณฑ์ตัดสิน (Anomaly Threshold หรือ Cutoff) มีผลโดยตรงต่อระบบคัดแยกชิ้นงานอย่างไร",
      "options": [
        "หากคะแนนสูงกว่าเกณฑ์จะตัดสินว่าเป็นชิ้นงานผิดปกติ (Fail/NG) หากต่ำกว่าเกณฑ์จะตัดสินว่าเป็นชิ้นงานปกติ (Pass)",
        "ไม่มีผลใด ๆ เนื่องจากโมเดลจะตัดสินผลลัพธ์เองโดยอัตโนมัติ",
        "ทำให้ภาพถ่ายถูกเปลี่ยนเป็นภาพขาวดำทันที",
        "เปลี่ยนระบบปฏิบัติการของบอร์ดพัฒนาเป็นระบบอื่น"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "เกณฑ์ Anomaly Threshold คือเส้นแบ่งตัดสิน หาก Anomaly Score เกินค่านี้ ระบบจะสรุปว่าเป็นของเสีย (NG) และหากต่ำกว่าค่านี้คือของปกติ (Pass)",
      "points": 1
    },
    {
      "id": "q_ch05_08",
      "quiz_uid": 48,
      "chapter_id": "ch05",
      "category": "chapter_quiz",
      "chapter_number": 5,
      "question_type": "multiple_choice",
      "question_text": "หากผู้พัฒนาตั้งค่าเกณฑ์ Anomaly Threshold ไว้ \"ต่ำเกินไป\" จะส่งผลเสียต่อการทำงานของระบบอย่างไร",
      "options": [
        "เกิด False Positive สูง คือ ชิ้นงานปกติอาจถูกตัดสินผิดพลาดว่าเป็นชิ้นงานชำรุด",
        "เกิด False Negative สูง คือ ชิ้นงานชำรุดทั้งหมดจะหลุดรอดผ่านเกณฑ์ไปได้",
        "กล้องดิจิทัลจะไม่สามารถส่งสัญญาณภาพสดได้",
        "โมเดลจะใช้เวลาในการประมวลผลนานขึ้นเป็น 10 เท่า"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "การตั้ง Threshold ต่ำเกินไปทำให้ระบบเข้มงวดเกินเหตุ ส่งผลให้ชิ้นงานที่ดีแต่มีแสงเงาเปลี่ยนไปเล็กน้อย ถูกตีตราว่าเป็นของเสีย (False Positive) โดยไม่จำเป็น",
      "points": 1
    },
    {
      "id": "q_ch05_09",
      "quiz_uid": 49,
      "chapter_id": "ch05",
      "category": "chapter_quiz",
      "chapter_number": 5,
      "question_type": "multiple_choice",
      "question_text": "ในขั้นตอนการประเมินประสิทธิภาพบนหน้าต่าง Model Testing ผู้พัฒนาควรเตรียมข้อมูลภาพชนิดใดมาใช้ทดสอบโมเดล",
      "options": [
        "ภาพที่มีทั้งชิ้นงานปกติและชิ้นงานที่มีตำหนิ/ความผิดปกติจริง ซึ่งโมเดลไม่เคยเห็นมาก่อน",
        "เฉพาะภาพชิ้นงานปกติที่คัดลอกมาจาก Training Set",
        "ภาพถ่ายวิวทิวทัศน์และธรรมชาติ",
        "ภาพเอกสารข้อความตัวหนังสือ"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "การทดสอบโมเดลความผิดปกติต้องใช้ทั้งภาพของดีและภาพของเสียที่โมเดลไม่เคยพบตอนเทรน เพื่อดูว่าโมเดลแยกแยะของเสียออกจากของดีได้แม่นยำหรือไม่",
      "points": 1
    },
    {
      "id": "q_ch05_10",
      "quiz_uid": 50,
      "chapter_id": "ch05",
      "category": "chapter_quiz",
      "chapter_number": 5,
      "question_type": "multiple_choice",
      "question_text": "ในสคริปต์ทดสอบ vad_test.py มีวัตถุประสงค์หลักในการประเมินระบบตามข้อใด",
      "options": [
        "ทดสอบการโหลดโมเดล Anomaly และจำลองการประมวลผลภาพเพื่อตรวจวัดค่าคะแนนความผิดปกติและความเร็ว",
        "ทดสอบการพิมพ์เอกสารผ่านเครื่องพิมพ์ไร้สาย",
        "ทดสอบการคำนวณราคาสินค้าในห้างสรรพสินค้า",
        "ทดสอบการเชื่อมต่ออุปกรณ์บลูทูธภายนอก"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "สคริปต์ vad_test.py ทำหน้าที่ทดสอบโหลดไฟล์โมเดล Anomaly ป้อนภาพทดสอบ และอ่านค่า Anomaly Score ออกมาเพื่อวัดความถูกต้องและความเร็วในการประมวลผล",
      "points": 1
    }
  ],

  6: [
    {
      "id": "q_ch06_01",
      "quiz_uid": 51,
      "chapter_id": "ch06",
      "category": "chapter_quiz",
      "chapter_number": 6,
      "question_type": "multiple_choice",
      "question_text": "เมื่อฝึกสอนโมเดลบน Edge Impulse เสร็จแล้ว หากต้องการนำไปรันบนระบบลีนุกซ์ของบอร์ด Arduino UNO Q ต้องเลือกประเภท Deployment เป็นรูปแบบใด",
      "options": [
        "Windows .exe Executable",
        "Linux (AArch64) หรือโมเดลไบนารี .eim",
        "Android APK Package",
        "WebAssembly (WASM)"
      ],
      "correct_index": 1,
      "correct_letter": "ข",
      "explanation": "บอร์ด Arduino UNO Q มีหน่วยประมวลผลหลักสถาปัตยกรรม 64 บิตบนระบบปฏิบัติการลีนุกซ์ จึงต้องเลือก Deployment เป็น Linux (AArch64) เพื่อรับไฟล์ .eim",
      "points": 1
    },
    {
      "id": "q_ch06_02",
      "quiz_uid": 52,
      "chapter_id": "ch06",
      "category": "chapter_quiz",
      "chapter_number": 6,
      "question_type": "multiple_choice",
      "question_text": "ไดเรกทอรีมาตรฐานบนระบบปฏิบัติการลีนุกซ์ของบอร์ด Arduino UNO Q ที่ใช้จัดเก็บไฟล์โมเดล .eim คือไดเรกทอรีใด",
      "options": [
        "/tmp/download",
        "/home/arduino/.arduino-bricks/ei-models",
        "/var/log/system",
        "/etc/network/interfaces"
      ],
      "correct_index": 1,
      "correct_letter": "ข",
      "explanation": "โฟลเดอร์มาตรฐานที่ระบบ Arduino App Lab และโมดูล Bricks ใช้ค้นหาไฟล์โมเดลปัญญาประดิษฐ์คือ /home/arduino/.arduino-bricks/ei-models",
      "points": 1
    },
    {
      "id": "q_ch06_03",
      "quiz_uid": 53,
      "chapter_id": "ch06",
      "category": "chapter_quiz",
      "chapter_number": 6,
      "question_type": "multiple_choice",
      "question_text": "เมื่อถ่ายโอนไฟล์โมเดล .eim ลงสู่บอร์ดแล้ว ต้องรันคำสั่งเทอร์มินัลใดเพื่อให้ระบบปฏิบัติการอนุญาตให้รันไฟล์ได้",
      "options": [
        "chmod +x <model_name>.eim",
        "rm -rf <model_name>.eim",
        "zip <model_name>.eim",
        "cat <model_name>.eim"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "คำสั่ง chmod +x เป็นการเพิ่มสิทธิ์การประมวลผล (Executable Permission) ให้แก่ไฟล์ในระบบปฏิบัติการลีนุกซ์ ทำให้ไฟล์ .eim สามารถถูกรันได้",
      "points": 1
    },
    {
      "id": "q_ch06_04",
      "quiz_uid": 54,
      "chapter_id": "ch06",
      "category": "chapter_quiz",
      "chapter_number": 6,
      "question_type": "multiple_choice",
      "question_text": "ไฟล์ app.yaml ในระบบของ Arduino App Lab ทำหน้าที่สำคัญตามข้อใด",
      "options": [
        "กำหนดค่าคอนฟิกูเรชัน ตัวแปรสภาพแวดล้อม และเชื่อมโยงโมเดลเข้ากับแอปพลิเคชัน",
        "ทำหน้าที่เก็บภาพถ่ายจากกล้องเว็บแคมทั้งหมด",
        "ทำหน้าที่เป็นโปรแกรมเล่นไฟล์เพลง MP3",
        "ทำหน้าที่ควบคุมความเร็วพัดลมซีพียู"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "ไฟล์ app.yaml เป็นไฟล์กำหนดค่าหลัก (Configuration File) ที่ใช้ประกาศตัวแปรสภาพแวดล้อม กำหนดพาธของโมเดล และตั้งค่าพารามิเตอร์ของ Brick",
      "points": 1
    },
    {
      "id": "q_ch06_05",
      "quiz_uid": 55,
      "chapter_id": "ch06",
      "category": "chapter_quiz",
      "chapter_number": 6,
      "question_type": "multiple_choice",
      "question_text": "โครงสร้างไวยากรณ์ล่าสุดในการประกาศพารามิเตอร์ในไฟล์ app.yaml ของ Arduino App Lab ต้องใช้สัญลักษณ์ใดครอบตัวแปร",
      "options": [
        "วงเล็บปีกกา { ... }",
        "เครื่องหมายคำพูดเดี่ยว ' ... '",
        "วงเล็บเหลี่ยม [ ... ]",
        "เครื่องหมายมากกว่าน้อยกว่า < ... >"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "มาตรฐานไวยากรณ์ล่าสุดของ app.yaml บน Arduino App Lab กำหนดให้ใช้โครงสร้างแบบวงเล็บปีกกา { ... } ในการระบุค่าพารามิเตอร์",
      "points": 1
    },
    {
      "id": "q_ch06_06",
      "quiz_uid": 56,
      "chapter_id": "ch06",
      "category": "chapter_quiz",
      "chapter_number": 6,
      "question_type": "multiple_choice",
      "question_text": "ตัวแปรสภาพแวดล้อมใดในไฟล์ app.yaml ที่ใช้สำหรับกำหนดที่อยู่ของไฟล์โมเดลตรวจจับความผิดปกติจากภาพ",
      "options": [
        "EI_ANOMALY_MODEL_PATH หรือตัวแปรเฉพาะของ Visual Anomaly Brick",
        "SOUND_VOLUME_LEVEL",
        "DISPLAY_SCREEN_RESOLUTION",
        "DATABASE_PORT_NUMBER"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "ตัวแปรโมเดลของ Visual Anomaly Brick ใช้ระบุชื่อไฟล์และพาธของโมเดล .eim เพื่อให้มอดูลตรวจจับความผิดปกติโหลดไปรันได้ถูกต้อง",
      "points": 1
    },
    {
      "id": "q_ch06_07",
      "quiz_uid": 57,
      "chapter_id": "ch06",
      "category": "chapter_quiz",
      "chapter_number": 6,
      "question_type": "multiple_choice",
      "question_text": "คำสั่งใดบนเทอร์มินัลลีนุกซ์ที่สามารถใช้ตรวจสอบว่าไฟล์โมเดล .eim เป็นไฟล์ไบนารีสำหรับสถาปัตยกรรม ARM AArch64 หรือไม่",
      "options": [
        "file <model_name>.eim",
        "echo <model_name>.eim",
        "touch <model_name>.eim",
        "diff <model_name>.eim"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "คำสั่ง file จะอ่านข้อมูลเฮดเดอร์ของไฟล์และแสดงคุณสมบัติ เช่น ELF 64-bit LSB executable, ARM aarch64 เพื่อยืนยันความถูกต้องของไฟล์ไบนารี",
      "points": 1
    },
    {
      "id": "q_ch06_08",
      "quiz_uid": 58,
      "chapter_id": "ch06",
      "category": "chapter_quiz",
      "chapter_number": 6,
      "question_type": "multiple_choice",
      "question_text": "หากผู้พัฒนาระบุชื่อไฟล์โมเดลในไฟล์ app.yaml ไม่ตรงกับชื่อไฟล์จริงในไดเรกทอรี จะส่งผลให้เกิดข้อผิดพลาดตามข้อใด",
      "options": [
        "ระบบจะแจ้งข้อผิดพลาดว่าไม่พบไฟล์โมเดล (File Not Found) และมอดูล Brick จะไม่สามารถเริ่มต้นทำงานได้",
        "ระบบจะดาวน์โหลดโมเดลใหม่จากอินเทอร์เน็ตให้โดยอัตโนมัติ",
        "บอร์ดพัฒนาจะตัดกระแสไฟและดับเครื่องทันที",
        "ไม่มีผลกระทบใด ๆ ระบบยังคงทำงานได้ตามปกติ"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "หากระบุชื่อไฟล์โมเดลผิด มอดูลจะไม่สามารถโหลดไฟล์เข้าหน่วยความจำได้ และจะเกิดข้อผิดพลาดในการรันแอปพลิเคชัน",
      "points": 1
    },
    {
      "id": "q_ch06_09",
      "quiz_uid": 59,
      "chapter_id": "ch06",
      "category": "chapter_quiz",
      "chapter_number": 6,
      "question_type": "multiple_choice",
      "question_text": "สคริปต์ fix_app_yaml.py ถูกพัฒนาขึ้นเพื่อวัตถุประสงค์ตามข้อใด",
      "options": [
        "ตรวจสอบและปรับแก้โครงสร้างไวยากรณ์ของไฟล์ app.yaml ให้ถูกต้องตามข้อกำหนดล่าสุดโดยอัตโนมัติ",
        "ลบไฟล์โมเดล .eim ทั้งหมดออกจากบอร์ด",
        "จัดรูปแบบตารางฐานข้อมูล SQLite ใหม่",
        "บันทึกไฟล์วิดีโอจากกล้องเว็บแคม"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "สคริปต์ fix_app_yaml.py ช่วยสแกนและแก้ไขโครงสร้างไวยากรณ์ไฟล์ app.yaml ป้องกันข้อผิดพลาดจากการพิมพ์วงเล็บหรือการเว้นวรรคผิด",
      "points": 1
    },
    {
      "id": "q_ch06_10",
      "quiz_uid": 60,
      "chapter_id": "ch06",
      "category": "chapter_quiz",
      "chapter_number": 6,
      "question_type": "multiple_choice",
      "question_text": "ข้อใดคือข้อได้เปรียบของการแยกไฟล์ตั้งค่า app.yaml ออกจากโค้ดโปรแกรมภาษาไพทอน",
      "options": [
        "สามารถปรับเปลี่ยนโมเดลหรือค่าพารามิเตอร์ได้สะดวกโดยไม่ต้องเข้าไปแก้ไขโค้ดโปรแกรมหลัก",
        "ช่วยให้ขนาดของโปรแกรมภาษาไพทอนเล็กลงจนไม่ต้องใช้พื้นที่จัดเก็บ",
        "ทำให้บอร์ดไม่จำเป็นต้องเชื่อมต่อกับกล้องดิจิทัล",
        "ป้องกันไม่ให้โปรแกรมทำงานซ้ำซ้อน"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "การแยก Configuration ออกจาก Source Code เป็นหลักการสากล ทำให้เปลี่ยนเวอร์ชันโมเดลหรือปรับจูนพารามิเตอร์ได้ง่ายโดยไม่ต้องแก้โค้ด",
      "points": 1
    }
  ],

  7: [
    {
      "id": "q_ch07_01",
      "quiz_uid": 61,
      "chapter_id": "ch07",
      "category": "chapter_quiz",
      "chapter_number": 7,
      "question_type": "multiple_choice",
      "question_text": "การเชื่อมต่อกล้องดิจิทัล UVC เข้ากับพอร์ต USB ของบอร์ด Arduino UNO Q สามารถตรวจสอบอุปกรณ์กล้องบนลีนุกซ์ได้ที่พาธใด",
      "options": [
        "/dev/video0 หรือ /dev/video1",
        "/etc/hosts",
        "/home/arduino/camera.txt",
        "/bin/camera_app"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "ระบบปฏิบัติการลีนุกซ์จะมองเห็นอุปกรณ์กล้องเว็บแคมมาตรฐาน UVC เป็นไฟล์อุปกรณ์ในไดเรกทอรี /dev/ เช่น /dev/video0",
      "points": 1
    },
    {
      "id": "q_ch07_02",
      "quiz_uid": 62,
      "chapter_id": "ch07",
      "category": "chapter_quiz",
      "chapter_number": 7,
      "question_type": "multiple_choice",
      "question_text": "ลูปการประมวลผลตรวจจับภาพสดแบบเวลาจริง (Real-Time Inference Loop) มีลำดับการทำงานตามข้อใด",
      "options": [
        "ดึงภาพจากกล้อง $\\rightarrow$ ส่งภาพให้โมเดลคำนวณคะแนน $\\rightarrow$ เปรียบเทียบกับเกณฑ์ $\\rightarrow$ สั่งงานฮาร์ดแวร์และบันทึกผล",
        "สั่งงานฮาร์ดแวร์ $\\rightarrow$ บันทึกผล $\\rightarrow$ ดึงภาพจากกล้อง $\\rightarrow$ ส่งภาพให้โมเดลคำนวณคะแนน",
        "ส่งภาพให้โมเดลคำนวณคะแนน $\\rightarrow$ ดึงภาพจากกล้อง $\\rightarrow$ สั่งงานฮาร์ดแวร์ $\\rightarrow$ ลบข้อมูล",
        "บันทึกผล $\\rightarrow$ เปรียบเทียบกับเกณฑ์ $\\rightarrow$ ปิดการทำงานของกล้อง $\\rightarrow$ เริ่มต้นใหม่"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "วงรอบการตรวจจับแบบเรียลไทม์จะเริ่มจากรับเฟรมภาพ $\\rightarrow$ นำเข้าสู่โมเดล $\\rightarrow$ ประเมินคะแนนเทียบเกณฑ์ $\\rightarrow$ ควบคุมเอาต์พุตและเก็บบันทึกประวัติ",
      "points": 1
    },
    {
      "id": "q_ch07_03",
      "quiz_uid": 63,
      "chapter_id": "ch07",
      "category": "chapter_quiz",
      "chapter_number": 7,
      "question_type": "multiple_choice",
      "question_text": "เมื่อโมเดล Visual Anomaly Detection คำนวณค่า Anomaly Max Score ออกมา โปรแกรมจะใช้เกณฑ์ใดตัดสินว่าเป็นชิ้นงานชำรุด (NG)",
      "options": [
        "เมื่อค่า Anomaly Max Score มีค่าสูงกว่าเกณฑ์ Threshold ที่กำหนดไว้",
        "เมื่อค่า Anomaly Max Score มีค่าเป็นศูนย์เท่านั้น",
        "เมื่อค่า Anomaly Max Score มีค่าน้อยกว่าเกณฑ์ Threshold",
        "เมื่อกล้องหยุดส่งสัญญาณภาพ"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "ในโมเดลตรวจจับความผิดปกติ คะแนนที่สูงแสดงถึงความแปลกแยกจากของปกติ หากคะแนนเกินเกณฑ์ Threshold ที่ตั้งไว้ จะตัดสินว่าเป็นชิ้นงานเสีย (NG/Fail)",
      "points": 1
    },
    {
      "id": "q_ch07_04",
      "quiz_uid": 64,
      "chapter_id": "ch07",
      "category": "chapter_quiz",
      "chapter_number": 7,
      "question_type": "multiple_choice",
      "question_text": "เมื่อระบบตรวจพบชิ้นงานชำรุด การสั่งงานสัญญาณเอาต์พุตเพื่อเตือนผู้ควบคุมเครื่องจักรสามารถทำได้ด้วยวิธีการใด",
      "options": [
        "ส่งสัญญาณควบคุมระดับสูง (HIGH) ไปยังขาสัญญาณดิจิทัล หรือแสดงสัญลักษณ์เตือนบน LED Matrix",
        "สั่งลบไฟล์โมเดลปัญญาประดิษฐ์ออกจากบอร์ด",
        "ปิดเครื่องคอมพิวเตอร์ของผู้ใช้ลงทันที",
        "ส่งอีเมลแจ้งผู้ผลิตบอร์ดในต่างประเทศ"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "การแจ้งเตือนทางกายภาพทำได้โดยส่งสัญญาณดิจิทัลออกไปยังหลอดไฟเตือน (Buzzer/Tower Lamp) หรือแสดงผลผ่านหน้าจอ LED Matrix ของบอร์ด",
      "points": 1
    },
    {
      "id": "q_ch07_05",
      "quiz_uid": 65,
      "chapter_id": "ch07",
      "category": "chapter_quiz",
      "chapter_number": 7,
      "question_type": "multiple_choice",
      "question_text": "การเชื่อมต่อระหว่าง Visual Anomaly Brick กับ Database-SQL Brick มีรูปแบบการทำงานอย่างไร",
      "options": [
        "เมื่อ Visual Anomaly Brick ได้ผลการทำนาย จะส่งค่าคะแนนและสถานะผ่านข้อความเหตุการณ์ไปให้ Database-SQL Brick บันทึกลงตาราง",
        "ทั้งสองมอดูลไม่สามารถทำงานร่วมกันได้บนบอร์ดเดียวกัน",
        "Database-SQL Brick จะทำหน้าที่เป็นกล้องส่งภาพให้โมเดล",
        "Visual Anomaly Brick จะลบข้อมูลทั้งหมดในฐานข้อมูลทิ้งก่อนเริ่มทำงาน"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "Visual Anomaly Brick ส่งข้อมูลเหตุการณ์ตรวจจับไปยัง Database-SQL Brick ผ่านกลไก Event-Driven เพื่อบันทึกประวัติลงฐานข้อมูลอย่างเป็นระบบ",
      "points": 1
    },
    {
      "id": "q_ch07_06",
      "quiz_uid": 66,
      "chapter_id": "ch07",
      "category": "chapter_quiz",
      "chapter_number": 7,
      "question_type": "multiple_choice",
      "question_text": "ข้อมูลชุดใดที่มีความสำคัญและควรบันทึกลงในฐานข้อมูล SQL ทุกครั้งที่โมเดลตรวจพบชิ้นงาน",
      "options": [
        "วันเวลา (Timestamp), สถานะผลตรวจ (Pass/Fail), และคะแนนความผิดปกติ (Anomaly Score)",
        "หมายเลขประจำเครื่องคอมพิวเตอร์ของครูผู้สอน",
        "ชื่อเครือข่ายอินเทอร์เน็ตที่เชื่อมต่อ",
        "ขนาดความจุของฮาร์ดดิสก์ทั้งหมด"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "ข้อมูลสาระสำคัญในการตรวจสอบคุณภาพ (QC Log) ต้องมี Timestamp, ผลการตรวจ (Pass/NG) และค่า Anomaly Score เพื่อใช้วิเคราะห์ย้อนหลัง",
      "points": 1
    },
    {
      "id": "q_ch07_07",
      "quiz_uid": 67,
      "chapter_id": "ch07",
      "category": "chapter_quiz",
      "chapter_number": 7,
      "question_type": "multiple_choice",
      "question_text": "เหตุใดในการตรวจจับภาพสดจากกล้องจึงควรมีกลไกหน่วงเวลาหรือการป้องกันการตรวจจับซ้ำ (Debounce Mechanism)",
      "options": [
        "เพื่อป้องกันไม่ให้ระบบบันทึกผลและแจ้งเตือนซ้ำซ้อนหลายครั้งในขณะที่ชิ้นงานชิ้นเดิมยังไม่เคลื่อนพ้นหน้ากล้อง",
        "เพื่อให้โมเดลมีเวลาพักระบายความร้อน 1 ชั่วโมง",
        "เพื่อลดความสว่างของแสงไฟในห้องปฏิบัติการ",
        "เพื่อทำให้ไฟล์ฐานข้อมูลมีขนาดใหญ่ขึ้น"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "กล้องวิดีโอส่งภาพหลายเฟรมต่อวินาที หากไม่มีกลไก Debounce ระบบจะตรวจจับชิ้นงานชิ้นเดิมซ้ำหลายครั้งในเสี้ยววินาที ทำให้สถิติคลาดเคลื่อน",
      "points": 1
    },
    {
      "id": "q_ch07_08",
      "quiz_uid": 68,
      "chapter_id": "ch07",
      "category": "chapter_quiz",
      "chapter_number": 7,
      "question_type": "multiple_choice",
      "question_text": "สคริปต์ test_vad_live.py มีบทบาทสำคัญในการทดสอบระบบตามข้อใด",
      "options": [
        "ทดสอบการรับภาพสดจากกล้อง ประมวลผลโมเดลความผิดปกติ และจำลองการแจ้งเตือนแบบเวลาจริง",
        "ทดสอบความเร็วในการดาวน์โหลดไฟล์จากอินเทอร์เน็ต",
        "ทดสอบการทำงานของเมาส์และคีย์บอร์ด",
        "ทดสอบการสำรองข้อมูลขึ้นสู่อีเมล"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "test_vad_live.py คือสคริปต์สำหรับรันระบบจริง เชื่อมกล้อง ประมวลผลภาพสด และทดสอบสัญญาณแจ้งเตือนร่วมกับฐานข้อมูล",
      "points": 1
    },
    {
      "id": "q_ch07_09",
      "quiz_uid": 69,
      "chapter_id": "ch07",
      "category": "chapter_quiz",
      "chapter_number": 7,
      "question_type": "multiple_choice",
      "question_text": "หากต้องการเขียนคำสั่ง SQL เพื่อสืบค้นหาว่ามีชิ้นงานที่ไม่ผ่านเกณฑ์ (status = 'NG') ทั้งหมดกี่ชิ้น ควรใช้คำสั่งใด",
      "options": [
        "SELECT COUNT(*) FROM qc_logs WHERE status = 'NG';",
        "COUNT ALL FROM qc_logs IF NG;",
        "SELECT SUM(status) FROM qc_logs;",
        "DELETE FROM qc_logs WHERE status = 'NG';"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "คำสั่ง SELECT COUNT(*) ร่วมกับเงื่อนไข WHERE status = 'NG' จะนับจำนวนแถวทั้งหมดที่บันทึกว่าชิ้นงานไม่ผ่านเกณฑ์",
      "points": 1
    },
    {
      "id": "q_ch07_10",
      "quiz_uid": 70,
      "chapter_id": "ch07",
      "category": "chapter_quiz",
      "chapter_number": 7,
      "question_type": "multiple_choice",
      "question_text": "การบูรณาการระบบ Visual Anomaly Detection เข้ากับ Local Database มีประโยชน์สูงสุดต่อภาคอุตสาหกรรมในด้านใด",
      "options": [
        "สร้างระบบตรวจสอบคุณภาพชิ้นงานอัตโนมัติที่มีหลักฐานข้อมูลย้อนหลังครบถ้วนโดยไม่ต้องพึ่งพาระบบคลาวด์ตลอดเวลา",
        "ช่วยประหยัดค่าวัสดุในการผลิตชิ้นงานลง 90%",
        "ทำให้ชิ้นงานที่ผลิตออกมาไม่มีวันแตกหักเสียหาย",
        "ลดจำนวนคนงานลงโดยไม่จำเป็นต้องมีการควบคุมดูแลใด ๆ"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "การตรวจจับของเสียอัตโนมัติพร้อมเก็บบันทึกประวัติบนบอร์ด ช่วยเพิ่มประสิทธิภาพการคัดแยกชิ้นงาน ตรวจสอบย้อนกลับได้ และทำงานได้ต่อเนื่องแบบออฟไลน์",
      "points": 1
    }
  ],

  8: [
    {
      "id": "q_ch08_01",
      "quiz_uid": 71,
      "chapter_id": "ch08",
      "category": "chapter_quiz",
      "chapter_number": 8,
      "question_type": "multiple_choice",
      "question_text": "ข้อใดอธิบายความแตกต่างระหว่างงาน Image Classification กับงาน Object Detection ได้ถูกต้องที่สุด",
      "options": [
        "Classification บอกเพียงชนิดของภาพรวม ส่วน Object Detection สามารถระบุทั้งชนิดและตำแหน่งพิกัดของวัตถุหลายชิ้นได้",
        "Classification ใช้กับภาพวิดีโอเท่านั้น ส่วน Object Detection ใช้กับภาพนิ่งเท่านั้น",
        "Classification ใช้เวลาในการประมวลผลนานกว่า Object Detection เสมอ",
        "Classification ตรวจจับวัตถุได้แม่นยำกว่า Object Detection ในทุกกรณี"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "Image Classification ทำหน้าที่จำแนกว่าภาพนี้คืออะไร (1 ภาพ 1 คำตอบ) ส่วน Object Detection จะค้นหาว่ามีวัตถุอะไรบ้าง และอยู่ที่ตำแหน่งใดในภาพ",
      "points": 1
    },
    {
      "id": "q_ch08_02",
      "quiz_uid": 72,
      "chapter_id": "ch08",
      "category": "chapter_quiz",
      "chapter_number": 8,
      "question_type": "multiple_choice",
      "question_text": "สถาปัตยกรรม FOMO (Faster Objects, More Objects) มีจุดเด่นสำคัญเหนือโมเดลตรวจจับวัตถุแบบดั้งเดิม (เช่น YOLO) ในเรื่องใด",
      "options": [
        "ใช้หน่วยความจำแรมน้อยมาก ประมวลผลได้รวดเร็ว เหมาะกับอุปกรณ์สมองกลฝังตัวที่มีทรัพยากรจำกัด",
        "สามารถตรวจจับวัตถุที่ซ้อนทับกันเป็นร้อยชิ้นได้อย่างสมบูรณ์แบบ",
        "ไม่จำเป็นต้องใช้ข้อมูลภาพในการฝึกสอนโมเดล",
        "สามารถทำงานได้โดยไม่ต้องมีเลนส์กล้อง"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "FOMO ได้รับการออกแบบมาเพื่อ Edge AI โดยเฉพาะ โดยลดการคำนวณที่ซับซ้อน ทำให้ใช้หน่วยความจำน้อยลงถึง 30 เท่า และรันได้เร็วกว่าโมเดลดั้งเดิมมาก",
      "points": 1
    },
    {
      "id": "q_ch08_03",
      "quiz_uid": 73,
      "chapter_id": "ch08",
      "category": "chapter_quiz",
      "chapter_number": 8,
      "question_type": "multiple_choice",
      "question_text": "ในขั้นตอนการติดป้ายกำกับข้อมูล (Bounding Box Labeling) บน Edge Impulse ผู้พัฒนาต้องกำหนดข้อมูลใดล้อมรอบวัตถุเป้าหมาย",
      "options": [
        "กรอบสี่เหลี่ยมระบุพิกัดแกน X, แกน Y, ความกว้าง (W), และความสูง (H)",
        "วงกลมระบุรัศมีรอบวัตถุ",
        "การระบายสีทับวัตถุทุกพิกเซล",
        "การพิมพ์ข้อความบรรยายความรู้สึกใต้ภาพ"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "การทำ Bounding Box คือการวาดกรอบสี่เหลี่ยมล้อมรอบวัตถุ ซึ่งจะบันทึกค่าพิกัดจุดเริ่มต้น (X, Y) พร้อมขนาดความกว้าง (Width) และความสูง (Height)",
      "points": 1
    },
    {
      "id": "q_ch08_04",
      "quiz_uid": 74,
      "chapter_id": "ch08",
      "category": "chapter_quiz",
      "chapter_number": 8,
      "question_type": "multiple_choice",
      "question_text": "ในหน้า Impulse Design บล็อกการเรียนรู้ (Learning Block) ที่ต้องเลือกสำหรับการสร้างโมเดล FOMO คือข้อใด",
      "options": [
        "Object Detection (Images)",
        "Classification (Keras)",
        "Regression Block",
        "Anomaly Detection (K-Means)"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "การสร้างโมเดลตรวจจับวัตถุ FOMO ต้องเลือก Learning Block เป็น Object Detection (Images)",
      "points": 1
    },
    {
      "id": "q_ch08_05",
      "quiz_uid": 75,
      "chapter_id": "ch08",
      "category": "chapter_quiz",
      "chapter_number": 8,
      "question_type": "multiple_choice",
      "question_text": "ผลลัพธ์จากการทำนายของโมเดลสถาปัตยกรรม FOMO จะส่งข้อมูลระบุตำแหน่งของวัตถุออกมาในรูปแบบใดเป็นหลัก",
      "options": [
        "พิกัดจุดกึ่งกลางของวัตถุ (Centroid X, Y) และความเชื่อมั่น (Confidence)",
        "ภาพสามมิติของวัตถุ",
        "คลื่นเสียงความถี่สูง",
        "ข้อความรหัส HTML"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "FOMO ตัดขั้นตอนการคำนวณขนาดกรอบที่ซับซ้อนออก โดยเน้นระบุพิกัดจุดกึ่งกลาง (Centroid X, Y) ของวัตถุ ทำให้คำนวณได้รวดเร็วมาก",
      "points": 1
    },
    {
      "id": "q_ch08_06",
      "quiz_uid": 76,
      "chapter_id": "ch08",
      "category": "chapter_quiz",
      "chapter_number": 8,
      "question_type": "multiple_choice",
      "question_text": "ในตารางเมทริกซ์ความสับสน (Confusion Matrix) แถบแนวทแยงมุมแสดงถึงข้อมูลข้อใด",
      "options": [
        "จำนวนการทำนายที่ถูกต้องของแต่ละคลาส (True Positives)",
        "จำนวนข้อมูลที่สูญหายระหว่างการส่งสัญญาณ",
        "อัตราการใช้พลังงานไฟฟ้าของระบบ",
        "จำนวนภาพที่ถูกลบออกจากโครงการ"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "แนวทแยงมุมในตาราง Confusion Matrix คือตำแหน่งที่คลาสเป้าหมายจริงตรงกับผลลัพธ์ที่โมเดลทำนาย ซึ่งแสดงถึงการทำนายที่ถูกต้อง",
      "points": 1
    },
    {
      "id": "q_ch08_07",
      "quiz_uid": 77,
      "chapter_id": "ch08",
      "category": "chapter_quiz",
      "chapter_number": 8,
      "question_type": "multiple_choice",
      "question_text": "ค่าความแม่นยำ (Precision) ในการตรวจจับวัตถุ มีความหมายตรงกับข้อใด",
      "options": [
        "สัดส่วนของวัตถุที่โมเดลทายว่าใช่ แล้วเป็นวัตถุนั้นจริง ๆ",
        "สัดส่วนของวัตถุจริงทั้งหมดที่โมเดลสามารถตามหาจนพบ",
        "ความเร็วในการรันโมเดลต่อหนึ่งวินาที",
        "ขนาดความจุของไฟล์โมเดลในหน่วยกิโลไบต์"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "Precision คือ สัดส่วนของสิ่งที่โมเดลตรวจพบว่าเป็นวัตถุนั้น แล้วถูกต้องจริง ๆ (True Positive / (True Positive + False Positive))",
      "points": 1
    },
    {
      "id": "q_ch08_08",
      "quiz_uid": 78,
      "chapter_id": "ch08",
      "category": "chapter_quiz",
      "chapter_number": 8,
      "question_type": "multiple_choice",
      "question_text": "หากระบบตรวจจับวัตถุเกิดปัญหา \"ตรวจพบวัตถุหลอกบ่อยครั้ง (False Positive)\" ผู้พัฒนาควรปรับแต่งค่าพารามิเตอร์ใด",
      "options": [
        "เพิ่มค่าเกณฑ์ความเชื่อมั่นขั้นต่ำ (Minimum Confidence Threshold)",
        "ลดค่าเกณฑ์ความเชื่อมั่นลงเป็น 0.05",
        "เปลี่ยนสายเชื่อมต่อ USB เส้นใหม่",
        "ปิดไฟในห้องปฏิบัติการให้มืดสนิท"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "การปรับเพิ่ม Confidence Threshold จะทำให้โมเดลรายงานผลเฉพาะวัตถุที่มั่นใจจริง ๆ ช่วยลดการตรวจพบสิ่งรบกวนหรือวัตถุหลอก (False Positive)",
      "points": 1
    },
    {
      "id": "q_ch08_09",
      "quiz_uid": 79,
      "chapter_id": "ch08",
      "category": "chapter_quiz",
      "chapter_number": 8,
      "question_type": "multiple_choice",
      "question_text": "สคริปต์ fomo_eval.py ถูกพัฒนาขึ้นเพื่อทำหน้าที่ใดในการทดสอบระบบ",
      "options": [
        "วัดและประเมินประสิทธิภาพของโมเดล FOMO ในด้านความแม่นยำและเวลาในการประมวลผล (Latency)",
        "สั่งซื้อสินค้าออนไลน์โดยอัตโนมัติ",
        "แปลภาษาจากภาษาอังกฤษเป็นภาษาไทย",
        "เพิ่มความละเอียดของภาพถ่ายจาก 720p เป็น 4K"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "fomo_eval.py ใช้สำหรับประเมินผลการตรวจจับของโมเดล FOMO ทั้งความถูกต้องเชิงสถิติและความเร็วในการประมวลผลบนฮาร์ดแวร์จริง",
      "points": 1
    },
    {
      "id": "q_ch08_10",
      "quiz_uid": 80,
      "chapter_id": "ch08",
      "category": "chapter_quiz",
      "chapter_number": 8,
      "question_type": "multiple_choice",
      "question_text": "ข้อใดเป็นข้อจำกัดสำคัญของสถาปัตยกรรม FOMO ที่ผู้พัฒนาต้องคำนึงถึงในการออกแบบระบบ",
      "options": [
        "ไม่เหมาะกับงานที่วัตถุอยู่ซ้อนทับกันอย่างหนาแน่น และไม่สามารถบอกขนาดกรอบสี่เหลี่ยมที่แน่นอนของวัตถุที่มีรูปร่างหลากหลายได้",
        "ไม่สามารถรันบนระบบปฏิบัติการลีนุกซ์ได้",
        "ไม่สามารถตรวจจับวัตถุที่มีสีได้",
        "ต้องใช้เวลาฝึกสอนนานกว่าโมเดลอื่นเป็นปี"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "FOMO เน้นหาจุดกึ่งกลาง (Centroid) จึงเหมาะกับวัตถุที่ขนาดใกล้เคียงกันและกระจายตัว ไม่เหมาะกับวัตถุที่ซ้อนทับกันมาก ๆ หรือวัตถุที่มีขนาดแตกต่างกันสุดขั้ว",
      "points": 1
    }
  ],

  9: [
    {
      "id": "q_ch09_01",
      "quiz_uid": 81,
      "chapter_id": "ch09",
      "category": "chapter_quiz",
      "chapter_number": 9,
      "question_type": "multiple_choice",
      "question_text": "ตัวแปรสภาพแวดล้อมใดในไฟล์ app.yaml ที่ใช้กำหนดพาธของโมเดลตรวจจับวัตถุ FOMO บน Arduino App Lab",
      "options": [
        "EI_OBJ_DETECTION_MODEL",
        "DATABASE_NAME",
        "SERIAL_BAUDRATE",
        "WIFI_SSID"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "EI_OBJ_DETECTION_MODEL คือตัวแปรสภาพแวดล้อมมาตรฐานที่ใช้กำหนดที่อยู่ของไฟล์โมเดลตรวจจับวัตถุ .eim ในไฟล์ app.yaml",
      "points": 1
    },
    {
      "id": "q_ch09_02",
      "quiz_uid": 82,
      "chapter_id": "ch09",
      "category": "chapter_quiz",
      "chapter_number": 9,
      "question_type": "multiple_choice",
      "question_text": "เมื่อโมเดล FOMO ตรวจพบวัตถุ ข้อมูลพิกัดตำแหน่งจุดกึ่งกลาง (Centroid) จะถูกส่งออกมาในรูปแบบของตัวแปรคู่ใด",
      "options": [
        "(x, y) หรือพิกัดแกนแนวนอนและแกนแนวตั้งบนภาพ",
        "(latitude, longitude) พิกัดดาวเทียม GPS",
        "(volt, ampere) ข้อมูลแรงดันและกระแสไฟฟ้า",
        "(red, blue) ข้อมูลสีของวัตถุ"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "ผลลัพธ์การตรวจจับของ FOMO ประกอบด้วยตำแหน่งพิกัดจุดกึ่งกลางของวัตถุบนภาพในระนาบแกน X (แนวนอน) และแกน Y (แนวตั้ง)",
      "points": 1
    },
    {
      "id": "q_ch09_03",
      "quiz_uid": 83,
      "chapter_id": "ch09",
      "category": "chapter_quiz",
      "chapter_number": 9,
      "question_type": "multiple_choice",
      "question_text": "การแปลงพิกัดจุดกึ่งกลาง (Centroid X) จากพิกเซลของภาพไปเป็นมุมการหมุนของเซอร์โวมอเตอร์ อาศัยหลักการทางคณิตศาสตร์ใด",
      "options": [
        "การเทียบสัดส่วนเชิงเส้น (Linear Mapping / Interpolation)",
        "การคำนวณอนุพันธ์ขั้นสูง (Calculus)",
        "การหาค่าลอการิทึมฐานสิบ",
        "การบวกเลขฐานสอง"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "การแปลงช่วงค่าจากความกว้างของภาพ (เช่น 0 ถึง 160 พิกเซล) ไปเป็นมุมของเซอร์โวมอเตอร์ (เช่น 0 ถึง 180 องศา) ใช้ฟังก์ชันการเทียบสัดส่วนเชิงเส้น (Linear Map)",
      "points": 1
    },
    {
      "id": "q_ch09_04",
      "quiz_uid": 84,
      "chapter_id": "ch09",
      "category": "chapter_quiz",
      "chapter_number": 9,
      "question_type": "multiple_choice",
      "question_text": "การกำหนดพื้นที่เป้าหมาย (Region of Interest: ROI) บนเฟรมภาพ มีประโยชน์อย่างไรต่อระบบคัดแยกชิ้นงาน",
      "options": [
        "สั่งให้อุปกรณ์ขับเคลื่อนทำงานเฉพาะเมื่อวัตถุเคลื่อนที่เข้ามาในตำแหน่งที่พร้อมคัดแยกเท่านั้น",
        "ทำให้กล้องสามารถมองเห็นภาพในเวลากลางคืนได้",
        "เพิ่มความละเอียดของภาพถ่ายให้คมชัดขึ้นสองเท่า",
        "ลดการใช้พลังงานไฟฟ้าของหลอดไฟในโรงงาน"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "การกำหนด ROI (ขอบเขตพื้นที่สนใจ) ช่วยให้ระบบสั่งงานกลไกผลักชิ้นงานเฉพาะตอนที่วัตถุเคลื่อนมาตรงกับตำแหน่งของอุปกรณ์คัดแยกพอดี",
      "points": 1
    },
    {
      "id": "q_ch09_05",
      "quiz_uid": 85,
      "chapter_id": "ch09",
      "category": "chapter_quiz",
      "chapter_number": 9,
      "question_type": "multiple_choice",
      "question_text": "อุปกรณ์ขับเคลื่อน (Actuator) ประเภทใดที่นิยมนำมาต่อใช้งานร่วมกับระบบเพื่อผลักคัดแยกชิ้นงานบนสายพาน",
      "options": [
        "เซอร์โวมอเตอร์ (Servo Motor) หรือกระบอกสูบลม (Pneumatic Cylinder)",
        "จอแสดงผลแบบ LCD",
        "ไมโครโฟนบันทึกเสียง",
        "เซนเซอร์วัดอุณหภูมิ"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "เซอร์โวมอเตอร์และกระบอกสูบลมคืออุปกรณ์ขับเคลื่อนทางกายภาพ (Actuator) ที่ใช้เปลี่ยนสัญญาณไฟฟ้าเป็นการเคลื่อนที่เพื่อผลักหรือคัดแยกชิ้นงาน",
      "points": 1
    },
    {
      "id": "q_ch09_06",
      "quiz_uid": 86,
      "chapter_id": "ch09",
      "category": "chapter_quiz",
      "chapter_number": 9,
      "question_type": "multiple_choice",
      "question_text": "หากสายพานลำเลียงเคลื่อนที่ด้วยความเร็วสูงกว่าความเร็วในการประมวลผล (Inference Speed) ของโมเดล จะส่งผลกระทบอย่างไร",
      "options": [
        "วัตถุอาจเคลื่อนที่ผ่านเลยตำแหน่งคัดแยกไปก่อนที่โมเดลจะประมวลผลเสร็จสิ้น (คัดแยกไม่ทัน)",
        "บอร์ดพัฒนาจะหยุดการทำงานทันที",
        "ภาพจากกล้องจะกลายเป็นภาพสีขาวดำ",
        "ทำให้โมเดลมีความแม่นยำสูงขึ้น"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "ความเร็วในการตรวจจับ (FPS) ต้องสัมพันธ์กับความเร็วของสายพาน หากสายพานเร็วเกินไป ชิ้นงานจะไหลผ่านกล้องไปก่อนที่ระบบจะส่งสัญญาณสั่งคัดแยก",
      "points": 1
    },
    {
      "id": "q_ch09_07",
      "quiz_uid": 87,
      "chapter_id": "ch09",
      "category": "chapter_quiz",
      "chapter_number": 9,
      "question_type": "multiple_choice",
      "question_text": "การเขียนโปรแกรมแบบ Event-driven Callback ในมอดูล Object Detection มีลักษณะการทำงานอย่างไร",
      "options": [
        "ฟังก์ชันตรวจจับจะถูกเรียกขึ้นมาทำงานโดยอัตโนมัติเฉพาะเมื่อตรวจพบวัตถุที่ตรงตามเงื่อนไข",
        "โปรแกรมจะต้องรอสัญญาณคำสั่งจากแป้นพิมพ์ของผู้ใช้ตลอดเวลา",
        "โปรแกรมจะหยุดทำงานเมื่อตรวจพบวัตถุ",
        "โปรแกรมจะส่งข้อมูลขึ้นระบบคลาวด์ทุก 1 ชั่วโมง"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "Event Callback จะทำงานทันทีเมื่อเกิดเหตุการณ์ (เช่น ตรวจพบวัตถุในพื้นที่เป้าหมาย) ช่วยให้โค้ดตอบสนองได้แบบเรียลไทม์และเป็นระเบียบ",
      "points": 1
    },
    {
      "id": "q_ch09_08",
      "quiz_uid": 88,
      "chapter_id": "ch09",
      "category": "chapter_quiz",
      "chapter_number": 9,
      "question_type": "multiple_choice",
      "question_text": "ในสคริปต์ fomo_live.py ฟังก์ชันใดที่ทำหน้าที่รับภาพสดจากกล้องและส่งพิกัดไปควบคุมระบบขับเคลื่อน",
      "options": [
        "ลูปตรวจจับหลักและการเรียกเมธอด on_detect() หรือ callback ที่กำหนดไว้",
        "คำสั่ง shutdown()",
        "คำสั่ง format_filesystem()",
        "คำสั่ง play_sound()"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "สคริปต์ fomo_live.py มีฟังก์ชันลูปประมวลผลเฟรมภาพสด และส่งพิกัดที่โมเดล FOMO ตรวจพบไปยังฟังก์ชัน Callback เพื่อควบคุม Actuator",
      "points": 1
    },
    {
      "id": "q_ch09_09",
      "quiz_uid": 89,
      "chapter_id": "ch09",
      "category": "chapter_quiz",
      "chapter_number": 9,
      "question_type": "multiple_choice",
      "question_text": "หากภาพจากกล้องมีการสั่นไหวเล็กน้อยทำให้พิกัดตรวจจับกระโดดไปมา เทคนิคใดช่วยแก้ปัญหาความไม่นิ่งของตำแหน่งได้",
      "options": [
        "การใช้ตัวกรองค่าเฉลี่ยเคลื่อนที่ (Moving Average Filter หรือ Coordinate Smoothing)",
        "การปิดการทำงานของบอร์ดพัฒนา",
        "การเพิ่มรอบการฝึกสอนโมเดลอีก 1,000 รอบ",
        "การลดความสว่างของหน้าจอคอมพิวเตอร์"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "Moving Average Filter หรือการทำ Smoothing พิกัด จะช่วยลดการกระตุกของค่าพิกัด ทำให้การสั่งงานเซอร์โวมอเตอร์ราบเรียบและนุ่มนวลขึ้น",
      "points": 1
    },
    {
      "id": "q_ch09_10",
      "quiz_uid": 90,
      "chapter_id": "ch09",
      "category": "chapter_quiz",
      "chapter_number": 9,
      "question_type": "multiple_choice",
      "question_text": "ระบบคัดแยกผลผลิตทางการเกษตร (เช่น ผลส้มดีและผลส้มเน่า) โดยใช้โมเดล FOMO และกระบอกสูบลม เป็นตัวอย่างการประยุกต์ใช้ Edge AI ในด้านใด",
      "options": [
        "เกษตรอัจฉริยะ (Smart Agriculture) และระบบอัตโนมัติในกระบวนการผลิต",
        "ระบบสารสนเทศเพื่อความบันเทิงในรถยนต์",
        "การพยากรณ์อากาศระดับโลก",
        "การทำธุรกรรมทางการเงินออนไลน์"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "การคัดแยกผลผลิตทางการเกษตรด้วยโมเดลวิทัศน์บนระบบสมองกลฝังตัวร่วมกับอุปกรณ์กลไก เป็นการประยุกต์ใช้งานด้านเกษตรอัจฉริยะและระบบคัดแยกอัตโนมัติ",
      "points": 1
    }
  ],

  10: [
    {
      "id": "q_ch10_01",
      "quiz_uid": 91,
      "chapter_id": "ch10",
      "category": "chapter_quiz",
      "chapter_number": 10,
      "question_type": "multiple_choice",
      "question_text": "รูปแบบผลลัพธ์ของงานจำแนกประเภทภาพ (Image Classification) มีลักษณะตามข้อใด",
      "options": [
        "หนึ่งป้ายกำกับต่อหนึ่งภาพ (One label per image) โดยบอกว่าภาพนั้นจัดอยู่ในหมวดหมู่ใดมากที่สุด",
        "พิกัดกล่องสี่เหลี่ยมรอบวัตถุทุกชิ้นในภาพ",
        "แผนที่ภูมิศาสตร์แสดงตำแหน่งของกล้อง",
        "การสร้างภาพวิดีโอใหม่จากภาพนิ่ง"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "Image Classification คือการกำหนดหมวดหมู่ให้กับภาพทั้งภาพ (Single Label) เช่น ภาพนี้เป็น ชิ้นงานสมบูรณ์ หรือ ชิ้นงานชำรุด",
      "points": 1
    },
    {
      "id": "q_ch10_02",
      "quiz_uid": 92,
      "chapter_id": "ch10",
      "category": "chapter_quiz",
      "chapter_number": 10,
      "question_type": "multiple_choice",
      "question_text": "เทคนิคการเรียนรู้แบบถ่ายโอน (Transfer Learning) มีข้อได้เปรียบหลักอย่างไรในการพัฒนาโมเดลบนอุปกรณ์ปลายทาง",
      "options": [
        "ใช้ประโยชน์จากแบบจำลองที่ผ่านการฝึกสอนกับชุดข้อมูลขนาดใหญ่มาแล้ว ทำให้ฝึกสอนโมเดลใหม่ได้เร็วและใช้ข้อมูลจำนวนน้อย",
        "ทำให้บอร์ดไม่ต้องใช้กระแสไฟฟ้าขณะประมวลผล",
        "ทำให้ภาพถ่ายกลายเป็นภาพสามมิติได้โดยอัตโนมัติ",
        "ป้องกันไม่ให้ไฟล์โมเดลถูกคัดลอกได้"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "Transfer Learning นำโครงข่ายที่มีความรู้พื้นฐานในการมองเห็นมาปรับใช้กับโจทย์ใหม่ จึงฝึกสอนได้เร็วมากและใช้รูปภาพตัวอย่างเพียงไม่กี่สิบภาพก็แม่นยำได้",
      "points": 1
    },
    {
      "id": "q_ch10_03",
      "quiz_uid": 93,
      "chapter_id": "ch10",
      "category": "chapter_quiz",
      "chapter_number": 10,
      "question_type": "multiple_choice",
      "question_text": "โครงสร้างโครงข่ายประสาทเทียมรุ่นใดที่นิยมนำมาใช้เป็นฐานสำหรับงาน Image Classification บนอุปกรณ์ขอบข่ายเนื่องจากมีขนาดเล็กและรันได้เร็ว",
      "options": [
        "MobileNetV2 (96x96 หรือ 160x160)",
        "GPT-4 Large Language Architecture",
        "AlexNet Original Architecture",
        "Inception-v4 Heavy Architecture"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "MobileNetV2 ได้รับการออกแบบโครงสร้างให้ประหยัดพลังประมวลผลและหน่วยความจำ เหมาะสำหรับการรันงานจำแนกประเภทภาพบนบอร์ดสมองกลฝังตัว",
      "points": 1
    },
    {
      "id": "q_ch10_04",
      "quiz_uid": 94,
      "chapter_id": "ch10",
      "category": "chapter_quiz",
      "chapter_number": 10,
      "question_type": "multiple_choice",
      "question_text": "การประยุกต์ใช้เทคนิค Data Augmentation (เช่น การหมุนภาพ พลิกภาพ ปรับความสว่าง) มีประโยชน์หลักตามข้อใด",
      "options": [
        "เพิ่มความหลากหลายให้แก่ชุดข้อมูลฝึกสอน ช่วยให้โมเดลไม่ยึดติดกับมุมมองเดิมและป้องกัน Overfitting",
        "ลดขนาดไฟล์ของภาพถ่ายให้เล็กลงครึ่งหนึ่ง",
        "เปลี่ยนภาพถ่ายสีให้กลายเป็นภาพขาวดำเสมอ",
        "ช่วยให้เลนส์กล้องมีความคมชัดมากขึ้น"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "Data Augmentation ช่วยจำลองสภาพการถ่ายภาพในมุมและแสงต่าง ๆ ทำให้โมเดลเรียนรู้คุณลักษณะที่แท้จริง ไม่ท่องจำเฉพาะมุมเดิม ป้องกันปัญหา Overfitting",
      "points": 1
    },
    {
      "id": "q_ch10_05",
      "quiz_uid": 95,
      "chapter_id": "ch10",
      "category": "chapter_quiz",
      "chapter_number": 10,
      "question_type": "multiple_choice",
      "question_text": "ฟังก์ชันกระตุ้น Softmax ในเลเยอร์สุดท้ายของโครงข่ายประสาทเทียมทำหน้าที่อะไร",
      "options": [
        "แปลงค่าผลลัพธ์การคำนวณของแต่ละคลาสให้อยู่ในรูปแบบของค่าความน่าจะเป็น (Probability) ที่มีผลรวมเท่ากับ 1.0",
        "สั่งลบข้อมูลในหน่วยความจำแคช",
        "ลดขนาดของภาพถ่ายลงเหลือ 1 พิกเซล",
        "ควบคุมความเร็วในการรับส่งข้อมูลผ่านพอร์ต USB"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "Softmax ทำหน้าที่แปลงค่าคะแนนดิบ (Logits) ให้กลายเป็นความน่าจะเป็นของแต่ละคลาส โดยผลรวมของทุกคลาสจะมีค่าเท่ากับ 1.0 (หรือ 100%)",
      "points": 1
    },
    {
      "id": "q_ch10_06",
      "quiz_uid": 96,
      "chapter_id": "ch10",
      "category": "chapter_quiz",
      "chapter_number": 10,
      "question_type": "multiple_choice",
      "question_text": "ตัวแปรสภาพแวดล้อมใดในไฟล์ app.yaml ที่ใช้กำหนดที่อยู่ของโมเดล Image Classification บนบอร์ดพัฒนา",
      "options": [
        "EI_CLASSIFICATION_MODEL",
        "ROBOT_SPEED_LIMIT",
        "LED_MATRIX_BRIGHTNESS",
        "SYSTEM_AUDIO_SOURCE"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "EI_CLASSIFICATION_MODEL เป็นตัวแปรมาตรฐานที่ใช้ชี้ไปยังไฟล์โมเดลจำแนกประเภทภาพ (.eim) ในไฟล์ตั้งค่า app.yaml",
      "points": 1
    },
    {
      "id": "q_ch10_07",
      "quiz_uid": 97,
      "chapter_id": "ch10",
      "category": "chapter_quiz",
      "chapter_number": 10,
      "question_type": "multiple_choice",
      "question_text": "ค่าความหน่วงในการประมวลผล (Inference Latency) มีความสัมพันธ์กับอัตราเฟรมเรต (FPS) ของระบบอย่างไร",
      "options": [
        "ยิ่งความหน่วงต่ำลง (ประมวลผลเร็วขึ้น) อัตราเฟรมเรตต่อวินาทีจะยิ่งสูงขึ้น ทำให้การตอบสนองราบรื่นขึ้น",
        "ยิ่งความหน่วงสูงขึ้น อัตราเฟรมเรตจะยิ่งสูงขึ้น",
        "ความหน่วงและอัตราเฟรมเรตไม่มีความสัมพันธ์กัน",
        "อัตราเฟรมเรตจะคงที่เท่ากับ 60 FPS เสมอไม่ว่าจะใช้โมเดลใด"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "Inference Latency คือเวลาที่ใช้ประมวลผลต่อ 1 ภาพ ยิ่งใช้เวลาน้อย ก็จะสามารถประมวลผลภาพได้จำนวนเฟรมต่อวินาที (FPS) มากขึ้น",
      "points": 1
    },
    {
      "id": "q_ch10_08",
      "quiz_uid": 98,
      "chapter_id": "ch10",
      "category": "chapter_quiz",
      "chapter_number": 10,
      "question_type": "multiple_choice",
      "question_text": "ในการสร้างชุดข้อมูลจำแนกประเภทภาพ เหตุใดจึงจำเป็นต้องมีคลาส \"Background\" หรือ \"Unknown\"",
      "options": [
        "เพื่อรองรับกรณีที่ไม่มีวัตถุเป้าหมายอยู่หน้ากล้อง ป้องกันไม่ให้โมเดลฝืนทำนายว่าเป็นคลาสอื่นโดยผิดพลาด",
        "เพื่อให้มีจำนวนคลาสเป็นเลขคู่เสมอ",
        "เพื่อเพิ่มความเร็วในการดาวน์โหลดโมเดล",
        "เพื่อให้ภาพถ่ายมีความสว่างมากขึ้น"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "หากไม่มีคลาส Background เมื่อหน้ากล้องว่างเปล่า โมเดลจะพยายามทายให้เข้าพวกกับคลาสใดคลาสหนึ่ง การมีคลาส Background ช่วยให้โมเดลบอกได้ว่าไม่มีวัตถุอยู่",
      "points": 1
    },
    {
      "id": "q_ch10_09",
      "quiz_uid": 99,
      "chapter_id": "ch10",
      "category": "chapter_quiz",
      "chapter_number": 10,
      "question_type": "multiple_choice",
      "question_text": "หากโมเดลทำนายภาพตัวอย่างด้วยค่าความเชื่อมั่นต่ำกว่าเกณฑ์ที่ตั้งไว้ (เช่น confidence < 0.6) โปรแกรมควรมีแนวทางจัดการอย่างไร",
      "options": [
        "จัดกลุ่มเป็นรายการที่ไม่แน่ชัด (Uncertain) และไม่สั่งให้อุปกรณ์ทำงาน เพื่อป้องกันการตัดสินใจผิดพลาด",
        "สั่งให้เครื่องจักรหยุดทำงานถาวร",
        "บังคับให้เลือกลำดับคลาสแรกเสมอ",
        "ลบโปรแกรมภาษาไพทอนทิ้ง"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "เมื่อโมเดลไม่มั่นใจ (Confidence ต่ำกว่าเกณฑ์) การตั้งสถานะเป็น Uncertain หรือรอผลในเฟรมถัดไป ช่วยป้องกันไม่ให้กลไกทางกายภาพสั่งงานผิดพลาด",
      "points": 1
    },
    {
      "id": "q_ch10_10",
      "quiz_uid": 100,
      "chapter_id": "ch10",
      "category": "chapter_quiz",
      "chapter_number": 10,
      "question_type": "multiple_choice",
      "question_text": "สคริปต์ classification_train.py ถูกออกแบบมาเพื่อสนับสนุนการทำงานในด้านใด",
      "options": [
        "ทดสอบและประเมินผลการจำแนกประเภทภาพสดผ่านกล้องพร้อมวัดความหน่วงของระบบ",
        "พิมพ์เอกสารสรุปคะแนนสอบของผู้เรียน",
        "ปรับความเร็วของพัดลมระบายความร้อน",
        "เขียนแบบจำลองสามมิติของอาคาร"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "สคริปต์ classification_train.py ใช้สำหรับทดสอบการทำนายผลของโมเดล Image Classification วัดความแม่นยำและเวลาในการประมวลผล",
      "points": 1
    }
  ],

  11: [
    {
      "id": "q_ch11_01",
      "quiz_uid": 101,
      "chapter_id": "ch11",
      "category": "chapter_quiz",
      "chapter_number": 11,
      "question_type": "multiple_choice",
      "question_text": "ระบบตรวจจับคำสั่งเสียงเฉพาะคำ (Keyword Spotting: KWS) มีหน้าที่หลักตามข้อใด",
      "options": [
        "ดักฟังและตรวจจับคำสั่งเสียงเฉพาะคำสั้น ๆ แบบเวลาจริง เช่น \"เปิดไฟ\" หรือ \"ปิดไฟ\"",
        "แปลบทความภาษาไทยทั้งเล่มให้กลายเป็นภาษาอังกฤษ",
        "บันทึกเสียงบทสนทนาตลอด 24 ชั่วโมงลงบนฮาร์ดดิสก์",
        "จำลองเสียงเครื่องดนตรีสากล"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "Keyword Spotting (KWS) ทำหน้าที่คอยดักจับเฉพาะคำสั่งเสียงสั้น ๆ ที่กำหนดไว้ล่วงหน้าเพื่อใช้สั่งการอุปกรณ์ เช่น คำสั่งเปิด-ปิด",
      "points": 1
    },
    {
      "id": "q_ch11_02",
      "quiz_uid": 102,
      "chapter_id": "ch11",
      "category": "chapter_quiz",
      "chapter_number": 11,
      "question_type": "multiple_choice",
      "question_text": "เทคนิค MFCC (Mel-Frequency Cepstral Coefficients) แปลงสัญญาณคลื่นเสียงในโดเมนเวลา (Time Domain) ให้อยู่ในรูปแบบใด",
      "options": [
        "ภาพสเปกโตรแกรมของสัมประสิทธิ์ความถี่ (2D Spectrogram Representation)",
        "ข้อความเอกสาร PDF",
        "ไฟล์รูปภาพสามมิติ",
        "สัญญาณไฟกระพริบ"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "MFCC สกัดคุณลักษณะของคลื่นเสียงให้อยู่ในรูปของภาพสเปกโตรแกรม 2 มิติ (แกนเวลาและแกนความถี่ Mel) เพื่อให้โครงข่ายประสาทเทียมประมวลผลต่อได้เหมือนภาพ",
      "points": 1
    },
    {
      "id": "q_ch11_03",
      "quiz_uid": 103,
      "chapter_id": "ch11",
      "category": "chapter_quiz",
      "chapter_number": 11,
      "question_type": "multiple_choice",
      "question_text": "เพราะเหตุใดสเกลความถี่แบบ Mel (Mel Scale) จึงเหมาะสมกับการสกัดคุณลักษณะของเสียงพูดมนุษย์",
      "options": [
        "เพราะจำลองลักษณะการได้ยินของหูมนุษย์ที่แยกแยะความถี่ต่ำได้ละเอียดกว่าความถี่สูง",
        "เพราะช่วยลดขนาดไฟล์เสียงลง 100 เท่า",
        "เพราะทำให้เสียงพูดมีระดับความดังเพิ่มขึ้น",
        "เพราะสามารถทำงานได้โดยไม่ต้องมีไมโครโฟน"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "หูของมนุษย์รับรู้ความแตกต่างของเสียงความถี่ต่ำได้ดีกว่าความถี่สูง สเกลแบบ Mel จึงเลียนแบบการได้ยินของมนุษย์ ทำให้จำแนกเสียงคำพูดได้แม่นยำมาก",
      "points": 1
    },
    {
      "id": "q_ch11_04",
      "quiz_uid": 104,
      "chapter_id": "ch11",
      "category": "chapter_quiz",
      "chapter_number": 11,
      "question_type": "multiple_choice",
      "question_text": "ในการฝึกสอนโมเดล KWS บน Edge Impulse ชุดข้อมูลเสียงที่สมบูรณ์จะต้องประกอบด้วยข้อมูล 3 คลาสสำคัญในข้อใด",
      "options": [
        "คลาสคำสั่งหลัก (Keyword), คลาสเสียงรบกวนพื้นหลัง (Noise), และคลาสคำพูดอื่นที่ไม่เกี่ยวข้อง (Unknown)",
        "คลาสเสียงเพลง, คลาสเสียงนก, และคลาสเสียงรถยนต์",
        "คลาสเสียงภาษาอังกฤษ, คลาสภาษาจีน, และคลาสภาษาฝรั่งเศส",
        "คลาสเสียงดัง, คลาสเสียงเบา, และคลาสเสียงเงียบ"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "โครงสร้างชุดข้อมูลเสียง KWS มาตรฐานต้องมี Keyword (คำสั่งที่ต้องการ), Noise (เสียงบรรยากาศรอบตัว) และ Unknown (คำพูดอื่น ๆ ที่ไม่ใช่คำสั่ง)",
      "points": 1
    },
    {
      "id": "q_ch11_05",
      "quiz_uid": 105,
      "chapter_id": "ch11",
      "category": "chapter_quiz",
      "chapter_number": 11,
      "question_type": "multiple_choice",
      "question_text": "ไฟล์เสียงตัวอย่างที่ใช้สำหรับฝึกสอนโมเดล Keyword Spotting ควรมีความยาวของคลิปเสียงประมาณเท่าใดจึงจะเหมาะสมที่สุด",
      "options": [
        "ประมาณ 1 วินาที (1,000 มิลลิวินาที)",
        "ประมาณ 1 ชั่วโมง",
        "ประมาณ 1 มิลลิวินาที",
        "ประมาณ 10 นาที"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "คำสั่งเสียงเฉพาะคำสั้น ๆ (เช่น \"เปิด\", \"ปิด\", \"หยุด\") มักมีความยาวไม่เกิน 1 วินาที จึงใช้หน้าต่างเวลามาตรฐานที่ 1 วินาที (1000 ms)",
      "points": 1
    },
    {
      "id": "q_ch11_06",
      "quiz_uid": 106,
      "chapter_id": "ch11",
      "category": "chapter_quiz",
      "chapter_number": 11,
      "question_type": "multiple_choice",
      "question_text": "บล็อกการเรียนรู้ (Learning Block) ชนิดใดที่นิยมนำมาใช้จำแนกภาพสเปกโตรแกรม MFCC ในระบบ Keyword Spotting",
      "options": [
        "Classification (1D/2D Convolutional Neural Network: CNN)",
        "Linear Regression",
        "K-Means Clustering",
        "Decision Tree Only"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "เมื่อสัญญาณเสียงถูกแปลงเป็นภาพสเปกโตรแกรม 2 มิติ โครงข่ายประสาทเทียมแบบคอนโวลูชัน (CNN) จะสามารถสกัดและจดจำลวดลายของเสียงได้อย่างยอดเยี่ยม",
      "points": 1
    },
    {
      "id": "q_ch11_07",
      "quiz_uid": 107,
      "chapter_id": "ch11",
      "category": "chapter_quiz",
      "chapter_number": 11,
      "question_type": "multiple_choice",
      "question_text": "ค่าอัตราการแจ้งเตือนผิดพลาด (False Activation Rate: FAR) ในระบบสั่งงานด้วยเสียง หมายถึงเหตุการณ์ใด",
      "options": [
        "การที่ไม่มีใครพูดคำสั่ง แต่ระบบกลับทำงานขึ้นมาเองเนื่องจากตีความเสียงรบกวนผิดพลาด",
        "การที่ผู้ใช้พูดคำสั่งถูกต้องชัดเจน แต่ระบบไม่ยอมตอบสนอง",
        "อัตราการสิ้นเปลืองกระแสไฟฟ้าของไมโครโฟน",
        "ความเร็วในการส่งสัญญาณเสียงผ่านสายเคเบิล"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "False Activation Rate (FAR) คือ อัตราที่ระบบทำงานผิดพลาดโดยตรวจจับเสียงอื่นหรือเสียงรบกวนแล้วเข้าใจผิดว่าเป็นคำสั่ง",
      "points": 1
    },
    {
      "id": "q_ch11_08",
      "quiz_uid": 108,
      "chapter_id": "ch11",
      "category": "chapter_quiz",
      "chapter_number": 11,
      "question_type": "multiple_choice",
      "question_text": "ตัวแปรสภาพแวดล้อมใดในไฟล์ app.yaml ที่ใช้ระบุไฟล์โมเดลตรวจจับคำสั่งเสียงบนบอร์ด Arduino UNO Q",
      "options": [
        "EI_KEYWORD_SPOTTING_MODEL",
        "DATABASE_PORT",
        "CAMERA_RESOLUTION",
        "WIFI_PASSWORD"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "EI_KEYWORD_SPOTTING_MODEL เป็นตัวแปรสภาพแวดล้อมมาตรฐานสำหรับกำหนดไฟล์โมเดล KWS (.eim) ในไฟล์ตั้งค่า app.yaml",
      "points": 1
    },
    {
      "id": "q_ch11_09",
      "quiz_uid": 109,
      "chapter_id": "ch11",
      "category": "chapter_quiz",
      "chapter_number": 11,
      "question_type": "multiple_choice",
      "question_text": "การตั้งค่าพารามิเตอร์ debounce_sec ในคลาส KeywordSpotting มีวัตถุประสงค์เพื่อป้องกันปัญหาใด",
      "options": [
        "ป้องกันไม่ให้ระบบรับคำสั่งซ้ำซ้อนติด ๆ กันหลายครั้งจากการพูดคำสั่งเพียงครั้งเดียว",
        "ป้องกันไม่ให้ไมโครโฟนร้อนเกินไป",
        "เพิ่มความดังของลำโพงแจ้งเตือน",
        "ลบไฟล์เสียงที่บันทึกทิ้งทันที"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "debounce_sec คือระยะเวลาหน่วงหลังจากตรวจพบคำสั่งแล้ว เพื่อไม่ให้โมเดลตอบสนองซ้ำกับเสียงหางคำเดิมที่ยังค้างอยู่ในไมโครโฟน",
      "points": 1
    },
    {
      "id": "q_ch11_10",
      "quiz_uid": 110,
      "chapter_id": "ch11",
      "category": "chapter_quiz",
      "chapter_number": 11,
      "question_type": "multiple_choice",
      "question_text": "ในสคริปต์ kws_features.py เมื่อตรวจจับคำสั่งเสียงภาษาไทยได้สำเร็จ สามารถนำสัญญาณไปสั่งการสิ่งใดได้ทันที",
      "options": [
        "ควบคุมเปิด-ปิดหลอดไฟ LED หรือสั่งงานวงจรรีเลย์เพื่อควบคุมเครื่องใช้ไฟฟ้า",
        "เปลี่ยนสีของตัวบอร์ดพัฒนา",
        "ปรับระดับความคมชัดของจอภาพ",
        "สั่งลบระบบปฏิบัติการลีนุกซ์"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "ผลลัพธ์จากการรู้จำคำสั่งเสียงสามารถส่งผ่านขาสัญญาณดิจิทัลของบอร์ดเพื่อควบคุมหลอดไฟ อุปกรณ์รีเลย์ หรือระบบเปิด-ปิดประตูได้แบบเวลาจริง",
      "points": 1
    }
  ],

  12: [
    {
      "id": "q_ch12_01",
      "quiz_uid": 111,
      "chapter_id": "ch12",
      "category": "chapter_quiz",
      "chapter_number": 12,
      "question_type": "multiple_choice",
      "question_text": "ข้อใดอธิบายความแตกต่างระหว่างงาน Keyword Spotting (KWS) กับงาน Audio Classification ได้ถูกต้องที่สุด",
      "options": [
        "KWS เน้นตรวจจับคำพูดเฉพาะคำสั้น ๆ ของมนุษย์ ส่วน Audio Classification ใช้จำแนกเสียงเหตุการณ์ทั่วไปหรือเสียงการทำงานของเครื่องจักร",
        "KWS ใช้กับเสียงดนตรีเท่านั้น ส่วน Audio Classification ใช้กับเสียงพูดเท่านั้น",
        "KWS ไม่ต้องใช้ไมโครโฟนในการรับเสียง",
        "Audio Classification ทำงานได้เฉพาะบนระบบคลาวด์เท่านั้น"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "KWS โฟกัสเฉพาะคำสั่งเสียงของมนุษย์ (เช่น คำสั่งควบคุม) ส่วน Audio Classification จำแนกเสียงอะคูสติกทั่วไป เช่น เสียงเครื่องจักรปกติ/ผิดปกติ เสียงกระจกแตก เสียงไซเรน",
      "points": 1
    },
    {
      "id": "q_ch12_02",
      "quiz_uid": 112,
      "chapter_id": "ch12",
      "category": "chapter_quiz",
      "chapter_number": 12,
      "question_type": "multiple_choice",
      "question_text": "การนำโมเดล Audio Classification ไปตรวจจับเสียงผิดปกติของตลับลูกปืนหรือมอเตอร์ในโรงงาน เป็นการประยุกต์ใช้งานในด้านใด",
      "options": [
        "การบำรุงรักษาเชิงคาดการณ์ (Predictive Maintenance)",
        "การแต่งเพลงและผลิตดนตรีสากล",
        "การจัดทำระบบแผนที่เดินทาง",
        "การจำหน่ายตั๋วโดยสารรถไฟ"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "การฟังเสียงเพื่อตรวจจับสัญญาณความผิดปกติก่อนที่เครื่องจักรจะชำรุดเสียหายหนัก เป็นหัวใจของระบบบำรุงรักษาเชิงคาดการณ์ (Predictive Maintenance)",
      "points": 1
    },
    {
      "id": "q_ch12_03",
      "quiz_uid": 113,
      "chapter_id": "ch12",
      "category": "chapter_quiz",
      "chapter_number": 12,
      "question_type": "multiple_choice",
      "question_text": "แนวคิดการบำรุงรักษาเชิงคาดการณ์ (Predictive Maintenance) มีข้อได้เปรียบเหนือการซ่อมเมื่อพัง (Reactive Maintenance) อย่างไร",
      "options": [
        "ช่วยป้องกันไม่ให้สายการผลิตต้องหยุดชะงักอย่างกะทันหัน และลดค่าใช้จ่ายในการซ่อมแซมใหญ่",
        "ทำให้เครื่องจักรทำงานได้โดยไม่ต้องใช้น้ำมันหล่อลื่น",
        "ทำให้โรงงานไม่ต้องจ่ายค่าไฟฟ้า",
        "ช่วยลดขนาดของเครื่องจักรลงครึ่งหนึ่ง"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "Predictive Maintenance ช่วยให้ตรวจพบความเสียหายตั้งแต่ระยะเริ่มต้น ทำให้วางแผนซ่อมบำรุงได้ทันท่วงที ไม่เกิดเหตุการณ์สายการผลิตหยุดชะงักโดยไม่คาดคิด",
      "points": 1
    },
    {
      "id": "q_ch12_04",
      "quiz_uid": 114,
      "chapter_id": "ch12",
      "category": "chapter_quiz",
      "chapter_number": 12,
      "question_type": "multiple_choice",
      "question_text": "สถาปัตยกรรมระบบปัญญาประดิษฐ์พหุโมดอล (Multi-Modal Edge AI) หมายถึงระบบที่มีลักษณะการทำงานตามข้อใด",
      "options": [
        "ระบบที่สามารถรับรู้และประมวลผลข้อมูลจากหลายประเภทเซนเซอร์พร้อมกัน เช่น การมองเห็นจากภาพ (Vision) ร่วมกับการได้ยินจากเสียง (Audio)",
        "ระบบที่ใช้เฉพาะบอร์ดพัฒนาโมเดลเดียวเท่านั้น",
        "ระบบที่ทำงานได้เฉพาะตอนกลางวันเท่านั้น",
        "ระบบที่ส่งข้อมูลผ่านสายเคเบิลเพียงเส้นเดียว"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "Multi-Modal AI คือการผสานข้อมูลมากกว่าหนึ่งรูปแบบ (เช่น ภาพจากกล้อง + เสียงจากไมโครโฟน) เพื่อให้ปัญญาประดิษฐ์ตัดสินใจได้อย่างรอบด้านและแม่นยำยิ่งขึ้น",
      "points": 1
    },
    {
      "id": "q_ch12_05",
      "quiz_uid": 115,
      "chapter_id": "ch12",
      "category": "chapter_quiz",
      "chapter_number": 12,
      "question_type": "multiple_choice",
      "question_text": "ข้อใดเป็นข้อได้เปรียบของการผสานข้อมูลจากกล้องตรวจจับภาพและไมโครโฟนตรวจจับเสียง (Sensor Fusion) บนบอร์ด Arduino UNO Q",
      "options": [
        "เพิ่มความน่าเชื่อถือในการตัดสินใจ เช่น เมื่อตรวจพบภาพชิ้นงานสะดุดและมีเสียงกระแทกดังพร้อมกัน ระบบจะมั่นใจได้ทันทีว่าเกิดอุบัติเหตุ",
        "ลดจำนวนสายไฟที่ต้องต่อเข้ากับตัวบอร์ด",
        "ทำให้ภาพถ่ายกลายเป็นภาพที่มีเสียงในตัวไฟล์เอง",
        "ช่วยเพิ่มความเร็วในการเชื่อมต่อ Wi-Fi"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "การใช้ทั้งภาพและเสียงร่วมกัน (Sensor Fusion) ช่วยลดความผิดพลาดในการตัดสินใจ หากมองเห็นภาพผิดปกติและได้ยินเสียงผิดปกติพร้อมกัน ความแม่นยำจะสูงขึ้นมาก",
      "points": 1
    },
    {
      "id": "q_ch12_06",
      "quiz_uid": 116,
      "chapter_id": "ch12",
      "category": "chapter_quiz",
      "chapter_number": 12,
      "question_type": "multiple_choice",
      "question_text": "เมื่อระบบ Multi-Modal AI ตรวจพบทั้งภาพชิ้นงานแตกหักและเสียงเครื่องจักรติดขัดพร้อมกัน ระบบควรดำเนินการอย่างไร",
      "options": [
        "ส่งสัญญาณหยุดการทำงานฉุกเฉิน (E-Stop), แจ้งเตือนผู้ควบคุม และบันทึกประวัติเหตุการณ์ลง Database-SQL Brick",
        "สั่งลบระบบฐานข้อมูลทิ้งทันที",
        "เร่งความเร็วของสายพานลำเลียงขึ้นเป็นสองเท่า",
        "ปิดสัญญาณไฟเตือนเพื่อไม่ให้เกิดเสียงรบกวน"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "เมื่อเกิดเหตุการณ์ผิดปกติขั้นวิกฤต ระบบความปลอดภัยต้องสั่งตัดการทำงาน แจ้งเตือนเจ้าหน้าที่ และบันทึกข้อมูลหลักฐานลงฐานข้อมูลทันที",
      "points": 1
    },
    {
      "id": "q_ch12_07",
      "quiz_uid": 117,
      "chapter_id": "ch12",
      "category": "chapter_quiz",
      "chapter_number": 12,
      "question_type": "multiple_choice",
      "question_text": "ในสคริปต์ multi_ai_live.py การประมวลผลทั้งโมเดลภาพและโมเดลเสียงพร้อมกันบนระบบลีนุกซ์ อาศัยกลไกการเขียนโปรแกรมใด",
      "options": [
        "การเขียนโปรแกรมแบบแยกเธรด (Multi-Threading) หรือการประมวลผลแบบอะซิงโครนัส (Asynchronous I/O)",
        "การเขียนโปรแกรมแบบหยุดรอทีละ 1 ชั่วโมง",
        "การสั่งให้ซีพียูปิดคอร์การทำงานเหลือเพียงคอร์เดียว",
        "การบันทึกโปรแกรมลงในแผ่นดิสก์"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "การรันโมเดลภาพและเสียงควบคู่กันต้องใช้ Multi-Threading หรือ Asynchronous Tasks เพื่อให้แต่ละลูปทำงานขนานกันบนซีพียูหลายคอร์ของบอร์ด UNO Q",
      "points": 1
    },
    {
      "id": "q_ch12_08",
      "quiz_uid": 118,
      "chapter_id": "ch12",
      "category": "chapter_quiz",
      "chapter_number": 12,
      "question_type": "multiple_choice",
      "question_text": "การสืบค้นข้อมูลประวัติเหตุการณ์ย้อนหลังผ่าน Database-SQL Brick มีบทบาทสำคัญต่อวิศวกรผู้ดูแลระบบในเรื่องใด",
      "options": [
        "วิเคราะห์แนวโน้มความถี่ของการเกิดเหตุการณ์ผิดปกติ และวางแผนปรับปรุงกระบวนการผลิตได้อย่างแม่นยำ",
        "ใช้คำนวณเงินเดือนของพนักงานทุกคน",
        "ใช้พิมพ์บัตรประจำตัวพนักงาน",
        "ใช้กำหนดราคาขายของสินค้าในท้องตลาด"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "ประวัติข้อมูลที่จัดเก็บอย่างเป็นระบบช่วยให้วิศวกรวิเคราะห์หารากเหง้าของปัญหา (Root Cause Analysis) และวางรอบการบำรุงรักษาเครื่องจักรได้อย่างมีหลักฐานอ้างอิง",
      "points": 1
    },
    {
      "id": "q_ch12_09",
      "quiz_uid": 119,
      "chapter_id": "ch12",
      "category": "chapter_quiz",
      "chapter_number": 12,
      "question_type": "multiple_choice",
      "question_text": "ข้อใดเป็นหลักจริยธรรมและความปลอดภัยที่สำคัญที่สุดในการติดตั้งระบบ Edge AI ที่มีเซนเซอร์ไมโครโฟนและกล้องในสถานประกอบการ",
      "options": [
        "การรักษาความเป็นส่วนตัว (Privacy) โดยประมวลผลข้อมูลที่ตัวอุปกรณ์ ไม่แอบบันทึกเสียงสนทนาส่วนบุคคล และมีป้ายแจ้งเตือนการใช้งานอย่างโปร่งใส",
        "การแอบบันทึกบทสนทนาของพนักงานทุกคนเก็บไว้เป็นความลับ",
        "การนำภาพถ่ายของทุกคนไปเผยแพร่บนสื่อสังคมออนไลน์",
        "การปิดไมโครโฟนไม่ให้บันทึกเสียงใด ๆ ในโรงงานเลย"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "จริยธรรมด้าน AI กำหนดให้ต้องเคารพสิทธิส่วนบุคคล ซึ่ง Edge AI ตอบโจทย์มากเนื่องจากประมวลผลเฉพาะในชิปโดยไม่ต้องส่งภาพ/เสียงดิบขึ้นอินเทอร์เน็ต และต้องแจ้งให้ผู้ปฏิบัติงานทราบอย่างโปร่งใส",
      "points": 1
    },
    {
      "id": "q_ch12_10",
      "quiz_uid": 120,
      "chapter_id": "ch12",
      "category": "chapter_quiz",
      "chapter_number": 12,
      "question_type": "multiple_choice",
      "question_text": "การบูรณาการระบบ Edge AI เข้ากับระบบสื่อสารไร้สาย (Wi-Fi / MQTT) นำไปสู่การพัฒนาเทคโนโลยีใดในอนาคต",
      "options": [
        "ระบบโรงงานอัจฉริยะ (Smart Factory) และอินเทอร์เน็ตของสรรพสิ่งในภาคอุตสาหกรรม (Industrial IoT)",
        "ระบบโทรเลขไร้สายแบบดั้งเดิม",
        "ระบบเครื่องรับวิทยุคลื่นสั้น",
        "ระบบเครื่องพิมพ์ดีดไฟฟ้า"
      ],
      "correct_index": 0,
      "correct_letter": "ก",
      "explanation": "การเชื่อมต่อระบบ Edge AI อัจฉริยะเข้ากับโครงข่ายไร้สายผ่านโปรโตคอล IoT เช่น MQTT เป็นรากฐานสำคัญของการยกระดับสู่อุตสาหกรรม 4.0 และ Smart Factory",
      "points": 1
    }
  ]
}

def update_json_databases():
    targets = [
        os.path.join('web_learning_platform', 'data', 'db.json'),
        os.path.join('web_learning_platform', 'data', 'seed.json'),
        os.path.join('web_learning_platform', 'data', 'db.backup.json')
    ]
    
    # Flatten all new quizzes from chapters 2 to 12
    all_new_ch2_to_12 = []
    for ch in range(2, 13):
        all_new_ch2_to_12.extend(CHAPTER_QUIZZES[ch])
        
    for target in targets:
        if not os.path.exists(target):
            continue
        with open(target, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        quizzes = data.get('quizzes', [])
        # Retain chapter 1 quizzes and midterm/final quizzes
        ch01_quizzes = [q for q in quizzes if q.get('chapter_id') == 'ch01' or (q.get('category') == 'chapter_quiz' and q.get('chapter_number') == 1)]
        midterm_final_quizzes = [q for q in quizzes if q.get('category') in ['midterm', 'final']]
        
        # Combine in exact order: ch01 (1-10), ch02-12 (11-120), midterm/final (121+)
        updated_quizzes = ch01_quizzes + all_new_ch2_to_12 + midterm_final_quizzes
        data['quizzes'] = updated_quizzes
        
        with open(target, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print(f"[OK] Updated {target} -> Total quizzes: {len(data['quizzes'])}")

def build_chapter_markdown(ch_num):
    title_map = {
        2: "สถาปัตยกรรมซอฟต์แวร์แบบมอดูล (Modular Brick) และการควบคุมฮาร์ดแวร์พื้นฐาน",
        3: "การจัดการระบบฐานข้อมูลบนอุปกรณ์ด้วย Database-SQL Brick",
        4: "การจัดเตรียมชุดข้อมูลและการออกแบบขั้นตอนการประมวลผล (Data Pipeline) บน Edge Impulse",
        5: "การฝึกสอนโมเดลตรวจจับความผิดปกติจากภาพ (Visual Anomaly Detection)",
        6: "การนำโมเดล .eim ไปใช้งานและการกำหนดค่าไฟล์ app.yaml บนบอร์ดพัฒนา Arduino UNO Q",
        7: "การประมวลผลโมเดลตรวจจับความผิดปกติจากภาพ และการบันทึกข้อมูลลง Database-SQL Brick",
        8: "การฝึกสอนโมเดลตรวจจับวัตถุด้วยสถาปัตยกรรม FOMO (Object Detection)",
        9: "การนำโมเดล FOMO ไปใช้งานและการควบคุมอุปกรณ์ขับเคลื่อน (Actuator)",
        10: "การพัฒนาและประมวลผลโมเดลจำแนกประเภทภาพ (Image Classification)",
        11: "การประมวลผลสัญญาณเสียงและการฝึกสอนโมเดลรู้จำคำสั่งเสียง (Keyword Spotting: KWS)",
        12: "การจำแนกเสียงเฉพาะทางและการบูรณาการระบบ Edge AI เชิงวิศวกรรม"
    }
    qs = CHAPTER_QUIZZES[ch_num]
    md = []
    md.append(f"# แบบทดสอบประจำบทที่ {ch_num}: {title_map[ch_num]}")
    md.append(f"**จำนวนข้อสอบ:** 10 ข้อ (แบบเลือกตอบ 4 ตัวเลือก ก, ข, ค, ง) | **เวลาในการทำแบบทดสอบ:** 20 นาที | **คะแนนเต็ม:** 10 คะแนน\n")
    
    for i, q in enumerate(qs, 1):
        md.append(f"#### {i}. {q['question_text']}")
        md.append(f"ก. {q['options'][0]}  ")
        md.append(f"ข. {q['options'][1]}  ")
        md.append(f"ค. {q['options'][2]}  ")
        md.append(f"ง. {q['options'][3]}  \n")
        
    md.append("---\n")
    md.append(f"### เฉลยคำตอบประจำบทที่ {ch_num}")
    for i, q in enumerate(qs, 1):
        md.append(f"{i}. **{q['correct_letter']}.** ({q['explanation']})")
    md.append("\n---\n")
    return "\n".join(md)

def update_markdown_120():
    path = "ข้อสอบปรนัย_แยกรายบท_120ข้อ.md"
    if not os.path.exists(path):
        return
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Keep header and Chapter 1
    # Locate where Chapter 1 ends
    p2 = content.find("# แบบทดสอบประจำบทที่ 2")
    if p2 == -1:
        p2 = content.find("แบบทดสอบประจำบทที่ 2")
    if p2 != -1:
        line_start = content.rfind('\n', 0, p2)
        prefix = content[:line_start+1] if line_start != -1 else content[:p2]
    else:
        print("[!] Could not find Chapter 2 marker in 120 MD")
        return
        
    # Generate all chapters 2 to 12
    chapters_md = []
    for ch in range(2, 13):
        chapters_md.append(build_chapter_markdown(ch))
        
    new_120_content = prefix + "\n" + "\n".join(chapters_md)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_120_content)
    print(f"[OK] Updated {path}")

def update_markdown_bank():
    path = "คลังข้อสอบปรนัย_ปัญญาประดิษฐ์สมองกลฝังตัว_รายบท.md"
    if not os.path.exists(path):
        return
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    p2 = content.find("# กลุ่มบทเรียนที่ 2:")
    if p2 == -1:
        p2 = content.find("กลุ่มบทเรียนที่ 2:")
    if p2 != -1:
        line_start = content.rfind('\n', 0, p2)
        prefix = content[:line_start+1] if line_start != -1 else content[:p2]
    else:
        print("[!] Could not find Group 2 marker in bank MD")
        return
        
    title_map = {
        2: "สถาปัตยกรรมซอฟต์แวร์แบบมอดูล (Modular Brick) และการควบคุมฮาร์ดแวร์พื้นฐาน",
        3: "การจัดการระบบฐานข้อมูลบนอุปกรณ์ด้วย Database-SQL Brick",
        4: "การจัดเตรียมชุดข้อมูลและการออกแบบขั้นตอนการประมวลผล (Data Pipeline) บน Edge Impulse",
        5: "การฝึกสอนโมเดลตรวจจับความผิดปกติจากภาพ (Visual Anomaly Detection)",
        6: "การนำโมเดล .eim ไปใช้งานและการกำหนดค่าไฟล์ app.yaml บนบอร์ดพัฒนา Arduino UNO Q",
        7: "การประมวลผลโมเดลตรวจจับความผิดปกติจากภาพ และการบันทึกข้อมูลลง Database-SQL Brick",
        8: "การฝึกสอนโมเดลตรวจจับวัตถุด้วยสถาปัตยกรรม FOMO (Object Detection)",
        9: "การนำโมเดล FOMO ไปใช้งานและการควบคุมอุปกรณ์ขับเคลื่อน (Actuator)",
        10: "การพัฒนาและประมวลผลโมเดลจำแนกประเภทภาพ (Image Classification)",
        11: "การประมวลผลสัญญาณเสียงและการฝึกสอนโมเดลรู้จำคำสั่งเสียง (Keyword Spotting: KWS)",
        12: "การจำแนกเสียงเฉพาะทางและการบูรณาการระบบ Edge AI เชิงวิศวกรรม"
    }
    
    groups_md = []
    for ch in range(2, 13):
        qs = CHAPTER_QUIZZES[ch]
        md = []
        md.append(f"# กลุ่มบทเรียนที่ {ch}: {title_map[ch]}\n")
        for i, q in enumerate(qs, 1):
            md.append(f"#### {i}. {q['question_text']}")
            md.append(f"ก. {q['options'][0]}  ")
            md.append(f"ข. {q['options'][1]}  ")
            md.append(f"ค. {q['options'][2]}  ")
            md.append(f"ง. {q['options'][3]}  \n")
            
        md.append("---\n")
        md.append(f"### เฉลยคำตอบและคำอธิบาย กลุ่มบทเรียนที่ {ch}\n")
        for i, q in enumerate(qs, 1):
            md.append(f"{i}. **เฉลย {q['correct_letter']}.**  \n   *คำอธิบาย:* {q['explanation']}")
        md.append("\n---\n")
        groups_md.append("\n".join(md))
        
    new_bank_content = prefix + "\n" + "\n".join(groups_md)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_bank_content)
    print(f"[OK] Updated {path}")

if __name__ == '__main__':
    update_json_databases()
    update_markdown_120()
    update_markdown_bank()

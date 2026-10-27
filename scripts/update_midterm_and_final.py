# -*- coding: utf-8 -*-
"""
Script to generate and update Midterm (Chapters 1-6) and Final (Chapters 7-12) exams across:
1. web_learning_platform/data/db.json
2. web_learning_platform/data/seed.json
3. web_learning_platform/data/db.backup.json
4. ข้อสอบกลางภาค_ปัญญาประดิษฐ์สมองกลฝังตัว_20ข้อ.md
5. ข้อสอบปลายภาค_ปัญญาประดิษฐ์สมองกลฝังตัว_20ข้อ.md
"""
import os
import sys
import json

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# 20 Midterm Questions (Chapters 1 - 6)
MIDTERM_QUESTIONS = [
  {
    "id": "q_mid_01",
    "quiz_uid": 121,
    "chapter_id": "midterm",
    "category": "midterm",
    "chapter_number": 0,
    "question_type": "multiple_choice",
    "question_text": "ข้อใดอธิบายความแตกต่างเชิงสถาปัตยกรรมระหว่าง \"ปัญญาประดิษฐ์บนอุปกรณ์ปลายทาง\" (Edge AI) กับ \"ปัญญาประดิษฐ์บนระบบคลาวด์\" (Cloud AI) ได้ถูกต้องที่สุด",
    "options": [
      "Edge AI ประมวลผลโมเดลบนฮาร์ดแวร์ปลายทางโดยตรง ทำให้ตอบสนองได้เร็ว ความหน่วงต่ำ และไม่ต้องส่งข้อมูลดิบออกนอกระบบ",
      "Edge AI ต้องเชื่อมต่ออินเทอร์เน็ตความเร็วสูงตลอดเวลาเพื่ออัปเดตโมเดลแบบเวลาจริง",
      "Cloud AI ตอบสนองได้เร็วกว่า Edge AI ในงานควบคุมเครื่องจักรแบบเวลาจริงระดับมิลลิวินาที",
      "Cloud AI รักษาความเป็นส่วนตัวของข้อมูลได้ดีกว่า Edge AI เนื่องจากไม่มีการบันทึกข้อมูลไว้ที่อุปกรณ์"
    ],
    "correct_index": 0,
    "correct_letter": "ก",
    "explanation": "Edge AI ประมวลผลบนอุปกรณ์โดยตรง จึงตอบสนองได้เร็วโดยมีความหน่วงต่ำมาก ทำงานแบบออฟไลน์ได้ และรักษาความปลอดภัยของข้อมูลดิบ",
    "points": 1
  },
  {
    "id": "q_mid_02",
    "quiz_uid": 122,
    "chapter_id": "midterm",
    "category": "midterm",
    "chapter_number": 0,
    "question_type": "multiple_choice",
    "question_text": "บอร์ดพัฒนา Arduino UNO Q ใช้สถาปัตยกรรมประมวลผลร่วม (Heterogeneous Computing) โดยผสานการทำงานระหว่างหน่วยประมวลผลใด",
    "options": [
      "MPU Qualcomm Dragonwing QRB2210 (Linux AArch64) และไมโครคอนโทรลเลอร์ ARM Cortex-M4",
      "ชิปประมวลผล Intel Core i7 ร่วมกับชิป ESP8266",
      "ไมโครคอนโทรลเลอร์ ATmega328P ทำงานร่วมกับชิป Bluetooth",
      "ชิป Raspberry Pi RP2040 ทำงานร่วมกับหน่วยความจำแฟลชภายนอก"
    ],
    "correct_index": 0,
    "correct_letter": "ก",
    "explanation": "บอร์ด UNO Q ใช้สถาปัตยกรรมไฮบริดระหว่าง MPU Qualcomm Dragonwing QRB2210 รัน Linux AArch64 และ MCU ARM Cortex-M4 ควบคุมฮาร์ดแวร์",
    "points": 1
  },
  {
    "id": "q_mid_03",
    "quiz_uid": 123,
    "chapter_id": "midterm",
    "category": "midterm",
    "chapter_number": 0,
    "question_type": "multiple_choice",
    "question_text": "ในการเชื่อมต่อบอร์ด Arduino UNO Q เข้าสู่เครือข่าย Wi-Fi นักเรียนสามารถเข้าถึงบอร์ดได้ผ่านชื่อโฮสต์ใด โดยไม่ต้องใช้หมายเลข IP Address",
    "options": [
      "arduino-uno-q.local",
      "arduino-board.org",
      "edge-impulse-q.net",
      "uno-q-server.com"
    ],
    "correct_index": 0,
    "correct_letter": "ก",
    "explanation": "ระบบรองรับโปรโตคอล mDNS ทำให้เรียกชื่อโฮสต์เป็น arduino-uno-q.local ในเครือข่ายเดียวกันได้ทันที",
    "points": 1
  },
  {
    "id": "q_mid_04",
    "quiz_uid": 124,
    "chapter_id": "midterm",
    "category": "midterm",
    "chapter_number": 0,
    "question_type": "multiple_choice",
    "question_text": "ข้อใดอธิบายแนวคิดของสถาปัตยกรรม \"Modular Brick\" บนซอฟต์แวร์ Arduino App Lab ได้ถูกต้องที่สุด",
    "options": [
      "การจัดโครงสร้างซอฟต์แวร์เป็นมอดูลอิสระที่แยกหน้าที่เฉพาะ และแลกเปลี่ยนข้อมูลผ่านระบบข้อความเหตุการณ์",
      "การเขียนคำสั่งควบคุมทั้งหมดไว้ในฟังก์ชันเดียวแบบเดิมเพื่อความกะทัดรัด",
      "การต่อวงจรอิเล็กทรอนิกส์ด้วยตัวต่อพลาสติกก่อนเสียบสายไฟ",
      "การแปลงโค้ดภาษาไพทอนให้กลายเป็นไฟล์ HTML"
    ],
    "correct_index": 0,
    "correct_letter": "ก",
    "explanation": "Modular Brick แบ่งซอฟต์แวร์ออกเป็นมอดูลอิสระที่ทำงานร่วมกันผ่าน Event/Message Passing ช่วยให้พัฒนาง่ายและยืดหยุ่น",
    "points": 1
  },
  {
    "id": "q_mid_05",
    "quiz_uid": 125,
    "chapter_id": "midterm",
    "category": "midterm",
    "chapter_number": 0,
    "question_type": "multiple_choice",
    "question_text": "ในการเขียนโปรแกรมภาษาไพทอนเพื่อรันแอปพลิเคชันบน Arduino App Lab คำสั่ง App.run() ทำหน้าที่สำคัญตามข้อใด",
    "options": [
      "เริ่มต้น Event Loop หลักของระบบเพื่อสั่งให้ทุกมอดูล Brick เริ่มต้นทำงานพร้อมกัน",
      "ลบไฟล์ขยะและแคชทั้งหมดออกจากหน่วยความจำของบอร์ด",
      "ตัดการเชื่อมต่อสัญญาณอินเทอร์เน็ตของบอร์ดทันที",
      "รีเซ็ตสิทธิ์ของไฟล์โมเดลปัญญาประดิษฐ์"
    ],
    "correct_index": 0,
    "correct_letter": "ก",
    "explanation": "App.run() ทำหน้าที่เริ่มต้น Event Loop หลักของระบบเพื่อสั่งให้ทุก Brick เริ่มต้นทำงานและรับส่งข้อมูลระหว่างกัน",
    "points": 1
  },
  {
    "id": "q_mid_06",
    "quiz_uid": 126,
    "chapter_id": "midterm",
    "category": "midterm",
    "chapter_number": 0,
    "question_type": "multiple_choice",
    "question_text": "การแสดงผลผ่านหลอดไฟ LED Matrix บนบอร์ด Arduino UNO Q มีวัตถุประสงค์หลักอย่างไรในระบบ Edge AI",
    "options": [
      "แสดงไอคอนสัญลักษณ์และกราฟิกแจ้งเตือนสถานะการทำงานของระบบให้ผู้ใช้ทราบทันที",
      "ทำหน้าที่เป็นเลนส์เสริมช่วยกล้องดิจิทัลในการโฟกัสภาพ",
      "ช่วยระบายความร้อนให้แก่ชิปประมวลผลหลัก Qualcomm",
      "เพิ่มความเร็วในการคำนวณของโครงข่ายประสาทเทียม"
    ],
    "correct_index": 0,
    "correct_letter": "ก",
    "explanation": "LED Matrix บนบอร์ดใช้แสดงสัญลักษณ์หรือไอคอนเพื่อสื่อสารสถานะการทำงาน (เช่น พร้อมทำงาน พบของเสีย เกิดข้อผิดพลาด) แก่ผู้ใช้งาน",
    "points": 1
  },
  {
    "id": "q_mid_07",
    "quiz_uid": 127,
    "chapter_id": "midterm",
    "category": "midterm",
    "chapter_number": 0,
    "question_type": "multiple_choice",
    "question_text": "มอดูล Database-SQL Brick บนบอร์ดพัฒนา Arduino UNO Q ใช้ระบบจัดการฐานข้อมูล (DBMS) ชนิดใดในการทำงาน",
    "options": [
      "SQLite ซึ่งเป็นระบบจัดการฐานข้อมูลเชิงสัมพันธ์แบบฝังตัว (Embedded Relational DB)",
      "Oracle Cloud Autonomous Database",
      "Microsoft SQL Server 2022",
      "MongoDB Distributed NoSQL Database"
    ],
    "correct_index": 0,
    "correct_letter": "ก",
    "explanation": "Database-SQL Brick ใช้ SQLite ซึ่งมีน้ำหนักเบา เก็บข้อมูลเป็นไฟล์เดียวบนระบบลีนุกซ์ เหมาะกับระบบสมองกลฝังตัว",
    "points": 1
  },
  {
    "id": "q_mid_08",
    "quiz_uid": 128,
    "chapter_id": "midterm",
    "category": "midterm",
    "chapter_number": 0,
    "question_type": "multiple_choice",
    "question_text": "คำสั่งภาษา SQL ในข้อใดใช้สำหรับสร้างตารางข้อมูลใหม่เพื่อจัดเก็บบันทึกประวัติการตรวจจับชิ้นงาน",
    "options": [
      "CREATE TABLE qc_records (...);",
      "NEW TABLE qc_records (...);",
      "ADD TABLE qc_records (...);",
      "MAKE TABLE qc_records (...);"
    ],
    "correct_index": 0,
    "correct_letter": "ก",
    "explanation": "CREATE TABLE เป็นคำสั่งมาตรฐานของภาษา SQL ในการสร้างโครงสร้างตารางข้อมูลใหม่",
    "points": 1
  },
  {
    "id": "q_mid_09",
    "quiz_uid": 129,
    "chapter_id": "midterm",
    "category": "midterm",
    "chapter_number": 0,
    "question_type": "multiple_choice",
    "question_text": "หากต้องการบันทึกผลการตรวจจับใหม่ลงในตารางฐานข้อมูล SQLite ต้องใช้คำสั่ง SQL ในข้อใด",
    "options": [
      "INSERT INTO qc_records (timestamp, label, score) VALUES (...);",
      "UPDATE qc_records SET label = (...);",
      "SELECT * FROM qc_records WHERE (...);",
      "ALTER TABLE qc_records ADD (...);"
    ],
    "correct_index": 0,
    "correct_letter": "ก",
    "explanation": "คำสั่ง INSERT INTO ใช้สำหรับเพิ่มแถวข้อมูลใหม่เข้าสู่ตารางฐานข้อมูล",
    "points": 1
  },
  {
    "id": "q_mid_10",
    "quiz_uid": 130,
    "chapter_id": "midterm",
    "category": "midterm",
    "chapter_number": 0,
    "question_type": "multiple_choice",
    "question_text": "หากต้องการสืบค้นจำนวนชิ้นงานที่ตรวจพบทั้งหมด โดยจัดกลุ่มแยกตามผลการตรวจสอบ (status) ควรเขียนคำสั่งตามข้อใด",
    "options": [
      "SELECT status, COUNT(*) FROM qc_records GROUP BY status;",
      "SELECT status, SUM(*) FROM qc_records ORDER BY status;",
      "SELECT COUNT(*) FROM qc_records WHERE status IS NULL;",
      "SELECT ALL FROM qc_records DIVIDE BY status;"
    ],
    "correct_index": 0,
    "correct_letter": "ก",
    "explanation": "การจัดกลุ่มเพื่อนับจำนวนข้อมูลแยกตามประเภทใช้ประโยค SELECT คอลัมน์, COUNT(*) ร่วมกับ GROUP BY คอลัมน์นั้น",
    "points": 1
  },
  {
    "id": "q_mid_11",
    "quiz_uid": 131,
    "chapter_id": "midterm",
    "category": "midterm",
    "chapter_number": 0,
    "question_type": "multiple_choice",
    "question_text": "ในขั้นตอนการเตรียมข้อมูล (Data Acquisition) อัตราส่วนมาตรฐานในการแบ่งชุดข้อมูลฝึกสอนต่อชุดข้อมูลทดสอบคือข้อใด",
    "options": [
      "80% สำหรับ Training Set และ 20% สำหรับ Testing Set",
      "50% สำหรับ Training Set และ 50% สำหรับ Testing Set",
      "95% สำหรับ Training Set และ 5% สำหรับ Testing Set",
      "100% สำหรับ Training Set โดยไม่ต้องมี Testing Set"
    ],
    "correct_index": 0,
    "correct_letter": "ก",
    "explanation": "อัตราส่วน 80:20 เป็นมาตรฐานสากลในแมชชีนเลิร์นนิง เพื่อให้โมเดลมีข้อมูลเรียนรู้เพียงพอและมีชุดข้อมูลทดสอบไว้วัดผลจริง",
    "points": 1
  },
  {
    "id": "q_mid_12",
    "quiz_uid": 132,
    "chapter_id": "midterm",
    "category": "midterm",
    "chapter_number": 0,
    "question_type": "multiple_choice",
    "question_text": "หากต้องการสร้างโมเดลตรวจจับความผิดปกติของชิ้นงาน (Visual Anomaly Detection) ต้องเลือกรูปแบบการติดป้ายกำกับในขั้นตอนสร้างโปรเจกต์อย่างไร",
    "options": [
      "One label per data item",
      "Bounding boxes (object detection)",
      "Multi-label regression",
      "Time-series audio"
    ],
    "correct_index": 0,
    "correct_letter": "ก",
    "explanation": "งาน Visual Anomaly Detection บนภาพชิ้นงานเดี่ยว ใช้รูปแบบ One label per data item ในการระบุป้ายกำกับของภาพชิ้นงาน",
    "points": 1
  },
  {
    "id": "q_mid_13",
    "quiz_uid": 133,
    "chapter_id": "midterm",
    "category": "midterm",
    "chapter_number": 0,
    "question_type": "multiple_choice",
    "question_text": "หากผู้พัฒนากำหนดขนาดมิติภาพใน Input Block ของ Impulse Design ให้มีขนาดใหญ่มากเกินไป จะส่งผลเสียอย่างไรต่อบอร์ด Arduino UNO Q",
    "options": [
      "โมเดลประมวลผลช้าลง ใช้แรมสูงขึ้น และเกิดความหน่วง (High Latency) ในการทำนายผล",
      "บอร์ดพัฒนาจะไม่สามารถเชื่อมต่อสัญญาณ Wi-Fi ได้",
      "ภาพถ่ายที่บันทึกจะกลายเป็นภาพสีขาวดำ",
      "ระบบฐานข้อมูล SQLite จะหยุดการทำงานทันที"
    ],
    "correct_index": 0,
    "correct_letter": "ก",
    "explanation": "ภาพขนาดใหญ่ต้องใช้การคำนวณมหาศาล ทำให้โมเดลรันช้าลง เปลืองหน่วยความจำแรม และเกิดความหน่วงสูง",
    "points": 1
  },
  {
    "id": "q_mid_14",
    "quiz_uid": 134,
    "chapter_id": "midterm",
    "category": "midterm",
    "chapter_number": 0,
    "question_type": "multiple_choice",
    "question_text": "หลักการสำคัญของการจำแนกประเภทข้อมูลแบบกลุ่มเดียว (One-Class Classification) ในงาน Visual Anomaly Detection คือข้อใด",
    "options": [
      "ฝึกสอนโมเดลด้วยภาพชิ้นงานปกติเท่านั้น และถือว่าสิ่งใดที่มีคุณลักษณะแปลกแยกออกไปคือความผิดปกติ",
      "ฝึกสอนโมเดลด้วยภาพชิ้นงานชำรุดทุกรูปแบบที่เป็นไปได้",
      "สุ่มเลือกผลการทำนายโดยไม่ต้องวิเคราะห์ภาพถ่าย",
      "แปลงข้อมูลภาพให้กลายเป็นคลื่นเสียงความถี่ต่ำ"
    ],
    "correct_index": 0,
    "correct_letter": "ก",
    "explanation": "One-Class Classification อาศัยการเรียนรู้คุณลักษณะของชิ้นงานปกติ (Good Items) เมื่อพบข้อมูลที่อยู่นอกกลุ่ม จะระบุว่าเป็นความผิดปกติทันที",
    "points": 1
  },
  {
    "id": "q_mid_15",
    "quiz_uid": 135,
    "chapter_id": "midterm",
    "category": "midterm",
    "chapter_number": 0,
    "question_type": "multiple_choice",
    "question_text": "สถาปัตยกรรมโมเดลตรวจจับความผิดปกติจากภาพที่ออกแบบมาเพื่ออุปกรณ์ขอบข่ายบนแพลตฟอร์ม Edge Impulse คือสถาปัตยกรรมใด",
    "options": [
      "FOMO-AD (Faster Objects, More Objects - Anomaly Detection)",
      "ResNet-152 Deep Network",
      "YOLOv8x Large Architecture",
      "BERT Transformer Network"
    ],
    "correct_index": 0,
    "correct_letter": "ก",
    "explanation": "FOMO-AD คือโมเดลตรวจจับความผิดปกติที่พัฒนาขึ้นเฉพาะสำหรับอุปกรณ์ Edge AI ขนาดเล็ก ใช้แรมน้อยและคำนวณได้เร็ว",
    "points": 1
  },
  {
    "id": "q_mid_16",
    "quiz_uid": 136,
    "chapter_id": "midterm",
    "category": "midterm",
    "chapter_number": 0,
    "question_type": "multiple_choice",
    "question_text": "หากผู้พัฒนาตั้งค่าเกณฑ์ตัดสินความผิดปกติ (Anomaly Threshold) ไว้ \"ต่ำเกินไป\" จะส่งผลกระทบอย่างไรต่อการคัดแยกชิ้นงาน",
    "options": [
      "เกิด False Positive สูง คือ ชิ้นงานปกติที่มีแสงเงาเปลี่ยนไปเล็กน้อยอาจถูกตัดสินว่าเป็นชิ้นงานชำรุด",
      "เกิด False Negative สูง คือ ชิ้นงานชำรุดทั้งหมดจะหลุดรอดผ่านการตรวจสอบไปได้",
      "กล้องดิจิทัลจะไม่สามารถรับสัญญาณภาพสดได้",
      "บอร์ดพัฒนาจะตัดการเชื่อมต่อกับระบบเครือข่าย"
    ],
    "correct_index": 0,
    "correct_letter": "ก",
    "explanation": "การตั้งเกณฑ์ Threshold ต่ำเกินไปทำให้ระบบเข้มงวดเกินเหตุ ชิ้นงานปกติที่มีความเบี่ยงเบนเล็กน้อยจะถูกตัดสินผิดพลาดว่าเป็นของเสีย (False Positive)",
    "points": 1
  },
  {
    "id": "q_mid_17",
    "quiz_uid": 137,
    "chapter_id": "midterm",
    "category": "midterm",
    "chapter_number": 0,
    "question_type": "multiple_choice",
    "question_text": "ไฟล์แบบจำลองปัญญาประดิษฐ์ที่คอมไพล์จาก Edge Impulse เพื่อนำไปรันบนระบบปฏิบัติการลีนุกซ์ของบอร์ด Arduino UNO Q มีนามสกุลไฟล์ใด",
    "options": [
      "`.eim` (Edge Impulse Model)",
      "`.apk`",
      "`.exe`",
      "`.hex`"
    ],
    "correct_index": 0,
    "correct_letter": "ก",
    "explanation": "ไฟล์ปฏิบัติการไบนารีของโมเดล AI บนลีนุกซ์สถาปัตยกรรม AArch64 จะใช้นามสกุล `.eim`",
    "points": 1
  },
  {
    "id": "q_mid_18",
    "quiz_uid": 138,
    "chapter_id": "midterm",
    "category": "midterm",
    "chapter_number": 0,
    "question_type": "multiple_choice",
    "question_text": "เมื่อโอนย้ายไฟล์โมเดล `.eim` ลงในโฟลเดอร์ `/home/arduino/.arduino-bricks/ei-models` แล้ว ต้องรันคำสั่งใดเพื่อให้ไฟล์สามารถรันประมวลผลได้",
    "options": [
      "chmod +x <model_name>.eim",
      "rm -rf <model_name>.eim",
      "unzip <model_name>.eim",
      "cat <model_name>.eim"
    ],
    "correct_index": 0,
    "correct_letter": "ก",
    "explanation": "คำสั่ง chmod +x เป็นการเพิ่มสิทธิ์การรัน (Executable Permission) ให้แก่ไฟล์ในระบบปฏิบัติการลีนุกซ์",
    "points": 1
  },
  {
    "id": "q_mid_19",
    "quiz_uid": 139,
    "chapter_id": "midterm",
    "category": "midterm",
    "chapter_number": 0,
    "question_type": "multiple_choice",
    "question_text": "โครงสร้างไวยากรณ์ล่าสุดในการกำหนดค่าพารามิเตอร์ในไฟล์ app.yaml บน Arduino App Lab ต้องใช้สัญลักษณ์ใดครอบตัวแปร",
    "options": [
      "วงเล็บปีกกา { ... }",
      "เครื่องหมายคำพูดเดี่ยว ' ... '",
      "วงเล็บเหลี่ยม [ ... ]",
      "เครื่องหมายดอกจัน * ... *"
    ],
    "correct_index": 0,
    "correct_letter": "ก",
    "explanation": "ไวยากรณ์ล่าสุดของ app.yaml บน Arduino App Lab กำหนดให้ใช้วงเล็บปีกกา { ... } ในการระบุค่าพารามิเตอร์ของระบบ",
    "points": 1
  },
  {
    "id": "q_mid_20",
    "quiz_uid": 140,
    "chapter_id": "midterm",
    "category": "midterm",
    "chapter_number": 0,
    "question_type": "multiple_choice",
    "question_text": "ข้อใดเป็นข้อได้เปรียบของการแยกไฟล์กำหนดค่า app.yaml ออกจากสคริปต์ภาษาไพทอน",
    "options": [
      "สามารถปรับเปลี่ยนโมเดล AI หรือค่าพารามิเตอร์ระบบได้สะดวกโดยไม่ต้องเข้าไปแก้ไขโค้ดโปรแกรมหลัก",
      "ช่วยลดขนาดไฟล์ของระบบปฏิบัติการลีนุกซ์ลงครึ่งหนึ่ง",
      "ทำให้บอร์ดไม่ต้องเชื่อมต่อสายไฟเลี้ยง",
      "ป้องกันไม่ให้กล้องตรวจจับภาพได้"
    ],
    "correct_index": 0,
    "correct_letter": "ก",
    "explanation": "การแยก Configuration ออกจาก Source Code ช่วยให้เปลี่ยนเวอร์ชันของโมเดลหรือปรับค่าระบบได้ง่ายโดยไม่ต้องแตะต้องโค้ดโปรแกรมหลัก",
    "points": 1
  }
]

# 20 Final Questions (Chapters 7 - 12)
FINAL_QUESTIONS = [
  {
    "id": "q_fin_01",
    "quiz_uid": 141,
    "chapter_id": "final",
    "category": "final",
    "chapter_number": 0,
    "question_type": "multiple_choice",
    "question_text": "เมื่อเชื่อมต่อกล้องเว็บแคม UVC เข้ากับพอร์ต USB ของบอร์ด Arduino UNO Q ระบบปฏิบัติการลีนุกซ์จะมองเห็นกล้องเป็นไฟล์อุปกรณ์ในข้อใด",
    "options": [
      "/dev/video0 หรือ /dev/video1",
      "/etc/camera.conf",
      "/var/log/video.log",
      "/home/arduino/camera.png"
    ],
    "correct_index": 0,
    "correct_letter": "ก",
    "explanation": "ระบบปฏิบัติการลีนุกซ์จะสร้างไฟล์อุปกรณ์สำหรับกล้องเว็บแคมในไดเรกทอรี /dev/ เช่น /dev/video0",
    "points": 1
  },
  {
    "id": "q_fin_02",
    "quiz_uid": 142,
    "chapter_id": "final",
    "category": "final",
    "chapter_number": 0,
    "question_type": "multiple_choice",
    "question_text": "ในระบบตรวจจับความผิดปกติจากภาพสด เหตุใดจึงต้องมีกลไกหน่วงเวลาหรือการตรวจสอบซ้ำ (Debounce Mechanism)",
    "options": [
      "เพื่อป้องกันไม่ให้ระบบส่งสัญญาณแจ้งเตือนและบันทึกประวัติซ้ำซ้อนในขณะที่ชิ้นงานชิ้นเดิมยังไม่เคลื่อนพ้นหน้ากล้อง",
      "เพื่อลดความร้อนของเลนส์กล้องดิจิทัล",
      "เพื่อให้โมเดลหยุดพักการทำงาน 1 ชั่วโมง",
      "เพื่อบังคับให้ชิ้นงานทุกชิ้นผ่านเกณฑ์การตรวจสอบ"
    ],
    "correct_index": 0,
    "correct_letter": "ก",
    "explanation": "กล้องส่งภาพหลายเฟรมต่อวินาที กลไก Debounce ช่วยป้องกันการบันทึกผลและแจ้งเตือนซ้ำกับชิ้นงานชิ้นเดิมที่ยังค้างอยู่หน้ากล้อง",
    "points": 1
  },
  {
    "id": "q_fin_03",
    "quiz_uid": 143,
    "chapter_id": "final",
    "category": "final",
    "chapter_number": 0,
    "question_type": "multiple_choice",
    "question_text": "เมื่อ Visual Anomaly Detection Brick ตรวจพบชิ้นงานชำรุด ระบบจะส่งข้อมูลไปบันทึกลง Database-SQL Brick ด้วยรูปแบบใด",
    "options": [
      "ส่งผ่านข้อความเหตุการณ์ (Event Message) เพื่อให้ Database Brick สั่งรันคำสั่ง INSERT INTO ลงตารางฐานข้อมูล",
      "สั่งลบไฟล์ฐานข้อมูลเดิมแล้วสร้างใหม่ทุกครั้ง",
      "ส่งอีเมลไปยังผู้ผลิตบอร์ดในต่างประเทศ",
      "บันทึกข้อมูลลงในแผ่นซีดีรอม"
    ],
    "correct_index": 0,
    "correct_letter": "ก",
    "explanation": "Visual Anomaly Brick ส่งข้อมูลเหตุการณ์ให้ Database Brick ดำเนินการ INSERT INTO บันทึกผลลง SQLite อย่างเป็นระบบ",
    "points": 1
  },
  {
    "id": "q_fin_04",
    "quiz_uid": 144,
    "chapter_id": "final",
    "category": "final",
    "chapter_number": 0,
    "question_type": "multiple_choice",
    "question_text": "ข้อใดอธิบายความแตกต่างระหว่างงาน Image Classification กับงาน Object Detection ได้ถูกต้องที่สุด",
    "options": [
      "Classification บอกเพียงว่าภาพรวมคืออะไร ส่วน Object Detection สามารถระบุทั้งชนิดและตำแหน่งพิกัดของวัตถุได้หลายชิ้น",
      "Classification ใช้สำหรับภาพสี ส่วน Object Detection ใช้ได้เฉพาะภาพขาวดำ",
      "Classification ตรวจจับวัตถุได้เร็วกว่า Object Detection เสมอในทุกสถาปัตยกรรม",
      "Classification สามารถสั่งการเซอร์โวมอเตอร์ได้แม่นยำกว่า Object Detection"
    ],
    "correct_index": 0,
    "correct_letter": "ก",
    "explanation": "Image Classification จำแนกหมวดหมู่ของภาพทั้งภาพ ส่วน Object Detection หาตำแหน่งพิกัดและชนิดของวัตถุหลายชิ้นในภาพ",
    "points": 1
  },
  {
    "id": "q_fin_05",
    "quiz_uid": 145,
    "chapter_id": "final",
    "category": "final",
    "chapter_number": 0,
    "question_type": "multiple_choice",
    "question_text": "สถาปัตยกรรม FOMO (Faster Objects, More Objects) มีจุดเด่นสำคัญเหนือโมเดลตรวจจับวัตถุแบบเดิมอย่างไร",
    "options": [
      "ใช้หน่วยความจำแรมน้อยลงอย่างมาก ประมวลผลได้รวดเร็ว เหมาะกับการทำงานบนอุปกรณ์สมองกลฝังตัว",
      "สามารถตรวจจับวัตถุที่มีขนาดเล็กกว่า 1 พิกเซลได้",
      "ไม่จำเป็นต้องมีข้อมูลภาพสำหรับฝึกสอนโมเดล",
      "สามารถมองเห็นวัตถุทะลุกำแพงได้"
    ],
    "correct_index": 0,
    "correct_letter": "ก",
    "explanation": "FOMO ถูกออกแบบมาเพื่อ Edge AI โดยลดความซับซ้อนของการคำนวณ ทำให้ใช้แรมน้อยลงและทำงานได้เร็วกว่าโมเดลตรวจจับวัตถุดั้งเดิมมาก",
    "points": 1
  },
  {
    "id": "q_fin_06",
    "quiz_uid": 146,
    "chapter_id": "final",
    "category": "final",
    "chapter_number": 0,
    "question_type": "multiple_choice",
    "question_text": "โมเดลตรวจจับวัตถุสถาปัตยกรรม FOMO จะส่งผลลัพธ์ตำแหน่งของวัตถุออกมาในรูปแบบใดเป็นหลัก",
    "options": [
      "พิกัดจุดกึ่งกลางของวัตถุ (Centroid X, Y) และค่าความเชื่อมั่น (Confidence)",
      "ภาพสามมิติของวัตถุ",
      "ไฟล์เสียงสังเคราะห์",
      "รหัสผ่านสำหรับการเชื่อมต่อเครือข่าย"
    ],
    "correct_index": 0,
    "correct_letter": "ก",
    "explanation": "FOMO ส่งค่าพิกัดจุดกึ่งกลาง (Centroid X, Y) ของวัตถุที่ตรวจพบ พร้อมค่าความเชื่อมั่นออกมาเป็นผลลัพธ์หลัก",
    "points": 1
  },
  {
    "id": "q_fin_07",
    "quiz_uid": 147,
    "chapter_id": "final",
    "category": "final",
    "chapter_number": 0,
    "question_type": "multiple_choice",
    "question_text": "หากระบบตรวจจับวัตถุเกิดปัญหาตรวจพบสิ่งรบกวนผิดพลาดว่าเป็นวัตถุเป้าหมาย (False Positive) บ่อยครั้ง ควรแก้ไขด้วยวิธีใด",
    "options": [
      "ปรับเพิ่มค่าเกณฑ์ความเชื่อมั่นขั้นต่ำ (Minimum Confidence Threshold)",
      "ลดค่าเกณฑ์ความเชื่อมั่นลงเป็น 0.01",
      "ถอดเลนส์กล้องออกแล้วใส่ใหม่",
      "เปลี่ยนสายพานลำเลียงให้มีสีสันมากขึ้น"
    ],
    "correct_index": 0,
    "correct_letter": "ก",
    "explanation": "การปรับเพิ่มค่าเกณฑ์ความเชื่อมั่น (Confidence Threshold) จะช่วยกรองวัตถุหลอกหรือสิ่งรบกวนที่มีความมั่นใจต่ำออกไป",
    "points": 1
  },
  {
    "id": "q_fin_08",
    "quiz_uid": 148,
    "chapter_id": "final",
    "category": "final",
    "chapter_number": 0,
    "question_type": "multiple_choice",
    "question_text": "ตัวแปรสภาพแวดล้อมใดในไฟล์ app.yaml ที่ใช้กำหนดที่อยู่ของโมเดลตรวจจับวัตถุ FOMO บนบอร์ดพัฒนา",
    "options": [
      "EI_OBJ_DETECTION_MODEL",
      "SERIAL_PORT_BAUDRATE",
      "AUDIO_SAMPLE_RATE",
      "SQLITE_DATABASE_PATH"
    ],
    "correct_index": 0,
    "correct_letter": "ก",
    "explanation": "EI_OBJ_DETECTION_MODEL คือตัวแปรมาตรฐานที่ใช้ชี้ไปยังไฟล์โมเดลตรวจจับวัตถุ (.eim) ในไฟล์ app.yaml",
    "points": 1
  },
  {
    "id": "q_fin_09",
    "quiz_uid": 149,
    "chapter_id": "final",
    "category": "final",
    "chapter_number": 0,
    "question_type": "multiple_choice",
    "question_text": "การแปลงพิกัดจุดกึ่งกลาง (Centroid X) จากพิกเซลของภาพไปเป็นมุมการหมุนของเซอร์โวมอเตอร์เพื่อคัดแยกวัตถุ อาศัยหลักการทางคณิตศาสตร์ใด",
    "options": [
      "การเทียบสัดส่วนเชิงเส้น (Linear Mapping / Interpolation)",
      "การหาปริพันธ์ขั้นสูง (Integration)",
      "การแก้สมการเชิงอนุพันธ์ย่อย",
      "การคำนวณเลขฐานสิบหก"
    ],
    "correct_index": 0,
    "correct_letter": "ก",
    "explanation": "การแปลงช่วงพิกเซลภาพ (เช่น 0-160) ไปเป็นช่วงองศาการหมุนของเซอร์โวมอเตอร์ (เช่น 0-180 องศา) ใช้ฟังก์ชันเทียบสัดส่วนเชิงเส้น (Linear Map)",
    "points": 1
  },
  {
    "id": "q_fin_10",
    "quiz_uid": 150,
    "chapter_id": "final",
    "category": "final",
    "chapter_number": 0,
    "question_type": "multiple_choice",
    "question_text": "การกำหนดพื้นที่สนใจ (Region of Interest: ROI) บนภาพสด มีประโยชน์อย่างไรต่อระบบคัดแยกชิ้นงานอัตโนมัติ",
    "options": [
      "ช่วยจำกัดขอบเขตและสั่งให้อุปกรณ์ขับเคลื่อนทำงานเฉพาะเมื่อวัตถุเคลื่อนเข้าสู่ตำแหน่งที่พร้อมคัดแยก",
      "ทำให้กล้องสามารถมองเห็นภาพในที่มืดได้ชัดเจนขึ้น",
      "ช่วยลดขนาดไฟล์ของระบบปฏิบัติการลีนุกซ์",
      "เพิ่มความเร็วในการหมุนของเซอร์โวมอเตอร์เป็นสองเท่า"
    ],
    "correct_index": 0,
    "correct_letter": "ก",
    "explanation": "ROI ช่วยให้ระบบคัดแยกทำงานอย่างแม่นยำ โดยสั่งงานกลไกผลักวัตถุเฉพาะตอนที่วัตถุเคลื่อนมาถึงตำแหน่งเป้าหมายพอดี",
    "points": 1
  },
  {
    "id": "q_fin_11",
    "quiz_uid": 151,
    "chapter_id": "final",
    "category": "final",
    "chapter_number": 0,
    "question_type": "multiple_choice",
    "question_text": "เทคนิคการเรียนรู้แบบถ่ายโอน (Transfer Learning) เช่น การใช้โครงสร้าง MobileNetV2 มีข้อได้เปรียบหลักตามข้อใด",
    "options": [
      "ใช้โมเดลที่ผ่านการฝึกสอนกับภาพจำนวนมากมาแล้ว ทำให้เรียนรู้งานใหม่ได้เร็วและใช้ภาพตัวอย่างจำนวนน้อย",
      "ทำให้บอร์ดไม่จำเป็นต้องต่อสายไฟเลี้ยง",
      "ทำให้ภาพถ่ายกลายเป็นภาพสามมิติได้โดยอัตโนมัติ",
      "ช่วยป้องกันไม่ให้ไฟล์โมเดลถูกลบ"
    ],
    "correct_index": 0,
    "correct_letter": "ก",
    "explanation": "Transfer Learning ดึงความรู้พื้นฐานจากโมเดลขนาดใหญ่มาต่อยอด ทำให้ฝึกสอนโมเดลใหม่ได้แม่นยำโดยใช้ภาพตัวอย่างเพียงไม่กี่ภาพ",
    "points": 1
  },
  {
    "id": "q_fin_12",
    "quiz_uid": 152,
    "chapter_id": "final",
    "category": "final",
    "chapter_number": 0,
    "question_type": "multiple_choice",
    "question_text": "ในการสร้างชุดข้อมูลสำหรับจำแนกประเภทภาพ (Image Classification) เหตุใดจึงจำเป็นต้องมีคลาส \"Background\" หรือ \"Unknown\"",
    "options": [
      "เพื่อป้องกันไม่ให้โมเดลฝืนทำนายผลเป็นคลาสอื่นเมื่อไม่มีวัตถุเป้าหมายปรากฏอยู่หน้ากล้อง",
      "เพื่อให้ระบบมีจำนวนคลาสเป็นเลขคู่เสมอ",
      "เพื่อเพิ่มขนาดไฟล์ภาพให้ใหญ่ขึ้น",
      "เพื่อปิดการทำงานของกล้องเมื่อไม่มีคนอยู่"
    ],
    "correct_index": 0,
    "correct_letter": "ก",
    "explanation": "คลาส Background ทำหน้าที่รองรับสภาวะที่ไม่มีวัตถุอยู่หน้ากล้อง ป้องกันไม่ให้โมเดลเดาผิดพลาดไปเป็นคลาสอื่น",
    "points": 1
  },
  {
    "id": "q_fin_13",
    "quiz_uid": 153,
    "chapter_id": "final",
    "category": "final",
    "chapter_number": 0,
    "question_type": "multiple_choice",
    "question_text": "ค่าความหน่วงในการประมวลผล (Inference Latency) มีความสัมพันธ์กับอัตราเฟรมเรตต่อวินาที (FPS) อย่างไร",
    "options": [
      "ยิ่งความหน่วงต่ำลง (ประมวลผลเร็วขึ้น) อัตราเฟรมเรตต่อวินาทีจะยิ่งสูงขึ้น ทำให้การตอบสนองราบรื่นขึ้น",
      "ยิ่งความหน่วงสูงขึ้น อัตราเฟรมเรตจะยิ่งสูงขึ้น",
      "ความหน่วงและอัตราเฟรมเรตไม่มีความเกี่ยวข้องกัน",
      "อัตราเฟรมเรตจะเท่ากับ 30 FPS เสมอไม่ว่าจะใช้โมเดลใด"
    ],
    "correct_index": 0,
    "correct_letter": "ก",
    "explanation": "Inference Latency คือเวลาในการประมวลผลต่อภาพ ยิ่งใช้เวลาน้อยลง ก็จะสามารถประมวลผลภาพได้จำนวนเฟรมต่อวินาที (FPS) มากขึ้น",
    "points": 1
  },
  {
    "id": "q_fin_14",
    "quiz_uid": 154,
    "chapter_id": "final",
    "category": "final",
    "chapter_number": 0,
    "question_type": "multiple_choice",
    "question_text": "เทคนิค MFCC (Mel-Frequency Cepstral Coefficients) ในระบบ Keyword Spotting ทำหน้าที่อะไรในกระบวนการทำงาน",
    "options": [
      "แปลงสัญญาณคลื่นเสียงให้เป็นภาพสเปกโตรแกรม 2 มิติที่จำลองลักษณะการได้ยินของหูมนุษย์",
      "เพิ่มระดับความดังของไมโครโฟนขึ้นเป็น 10 เท่า",
      "แปลคำพูดภาษาไทยให้เป็นตัวอักษรภาษาอังกฤษ",
      "บันทึกเสียงลงในหน่วยความจำแฟลช"
    ],
    "correct_index": 0,
    "correct_letter": "ก",
    "explanation": "MFCC ทำหน้าที่สกัดคุณลักษณะของสัญญาณเสียงให้อยู่ในรูปของภาพสเปกโตรแกรม 2 มิติตามสเกล Mel เพื่อให้โครงข่าย CNN ประมวลผลต่อได้",
    "points": 1
  },
  {
    "id": "q_fin_15",
    "quiz_uid": 155,
    "chapter_id": "final",
    "category": "final",
    "chapter_number": 0,
    "question_type": "multiple_choice",
    "question_text": "ชุดข้อมูลเสียงที่สมบูรณ์สำหรับการฝึกสอนโมเดล Keyword Spotting จะต้องประกอบด้วย 3 คลาสสำคัญตามข้อใด",
    "options": [
      "คำสั่งหลัก (Keyword), เสียงรบกวนพื้นหลัง (Noise), และคำพูดอื่นที่ไม่เกี่ยวข้อง (Unknown)",
      "เสียงผู้ชาย, เสียงผู้หญิง, และเสียงเด็ก",
      "เสียงดนตรี, เสียงสัตว์, และเสียงธรรมชาติ",
      "เสียงดัง, เสียงปานกลาง, และเสียงเบา"
    ],
    "correct_index": 0,
    "correct_letter": "ก",
    "explanation": "ชุดข้อมูล KWS ที่สมบูรณ์ต้องมีคลาสคำสั่ง (Keyword) คลาสเสียงรบกวน (Noise) และคลาสคำพูดอื่น ๆ (Unknown)",
    "points": 1
  },
  {
    "id": "q_fin_16",
    "quiz_uid": 156,
    "chapter_id": "final",
    "category": "final",
    "chapter_number": 0,
    "question_type": "multiple_choice",
    "question_text": "การกำหนดค่าพารามิเตอร์ debounce_sec ในคลาส KeywordSpotting มีประโยชน์สำคัญในด้านใด",
    "options": [
      "ป้องกันไม่ให้ระบบรับคำสั่งซ้ำซ้อนหลายครั้งติด ๆ กันจากการออกเสียงคำสั่งเพียงครั้งเดียว",
      "ป้องกันไม่ให้ไมโครโฟนเกิดเสียงหวีดสะท้อน",
      "ช่วยลดขนาดไฟล์ของโมเดลเสียง",
      "ขยายระยะการรับเสียงของไมโครโฟนให้ไกลขึ้น"
    ],
    "correct_index": 0,
    "correct_letter": "ก",
    "explanation": "debounce_sec ช่วยหน่วงเวลาหลังจากรับคำสั่งแล้ว เพื่อไม่ให้โมเดลตอบสนองซ้ำกับเสียงหางคำเดิมที่ยังค้างอยู่ในไมโครโฟน",
    "points": 1
  },
  {
    "id": "q_fin_17",
    "quiz_uid": 157,
    "chapter_id": "final",
    "category": "final",
    "chapter_number": 0,
    "question_type": "multiple_choice",
    "question_text": "ข้อใดอธิบายความแตกต่างระหว่างงาน Keyword Spotting กับงาน Audio Classification ได้ถูกต้องที่สุด",
    "options": [
      "Keyword Spotting ตรวจจับคำสั่งเสียงพูดสั้น ๆ ส่วน Audio Classification จำแนกเสียงเหตุการณ์หรือเสียงเครื่องจักรทั่วไป",
      "Keyword Spotting ใช้กับเสียงสัตว์ ส่วน Audio Classification ใช้กับเสียงคน",
      "Keyword Spotting ไม่ต้องใช้ไมโครโฟน",
      "Audio Classification ไม่สามารถรันบนระบบลีนุกซ์ได้"
    ],
    "correct_index": 0,
    "correct_letter": "ก",
    "explanation": "Keyword Spotting เน้นเฉพาะคำสั่งเสียงพูดของมนุษย์ ส่วน Audio Classification จำแนกเสียงอะคูสติกทั่วไป เช่น เสียงเครื่องจักรปกติ/ผิดปกติ เสียงกระจกแตก",
    "points": 1
  },
  {
    "id": "q_fin_18",
    "quiz_uid": 158,
    "chapter_id": "final",
    "category": "final",
    "chapter_number": 0,
    "question_type": "multiple_choice",
    "question_text": "การประยุกต์ใช้โมเดล Audio Classification เพื่อตรวจจับเสียงความผิดปกติของมอเตอร์ในโรงงาน มีบทบาทสำคัญต่อระบบใด",
    "options": [
      "การบำรุงรักษาเชิงคาดการณ์ (Predictive Maintenance) เพื่อลดความเสี่ยงที่สายการผลิตจะหยุดชะงัก",
      "การจัดทำระบบแผนที่เดินทางอัจฉริยะ",
      "การคำนวณเงินเดือนของพนักงาน",
      "การปรับระดับเสียงเพลงในโรงอาหาร"
    ],
    "correct_index": 0,
    "correct_letter": "ก",
    "explanation": "การดักฟังเสียงเครื่องจักรเพื่อเตือนความผิดปกติก่อนที่เครื่องจักรจะชำรุดเสียหายหนัก เป็นหัวใจของระบบ Predictive Maintenance",
    "points": 1
  },
  {
    "id": "q_fin_19",
    "quiz_uid": 159,
    "chapter_id": "final",
    "category": "final",
    "chapter_number": 0,
    "question_type": "multiple_choice",
    "question_text": "สถาปัตยกรรมระบบปัญญาประดิษฐ์พหุโมดอล (Multi-Modal Edge AI) หมายถึงระบบที่มีลักษณะการทำงานตามข้อใด",
    "options": [
      "ระบบที่สามารถรับรู้และผสานข้อมูลจากหลายประเภทเซนเซอร์พร้อมกัน เช่น การมองเห็นจากภาพร่วมกับการได้ยินจากเสียง",
      "ระบบที่ต้องใช้เฉพาะบอร์ดพัฒนาโมเดลเดียวเท่านั้น",
      "ระบบที่ทำงานได้เฉพาะเวลาที่ไม่มีแสงสว่าง",
      "ระบบที่ส่งข้อมูลผ่านสัญญาณคลื่นวิทยุ AM"
    ],
    "correct_index": 0,
    "correct_letter": "ก",
    "explanation": "Multi-Modal AI คือการผสานข้อมูลมากกว่าหนึ่งรูปแบบ (เช่น ภาพจากกล้อง + เสียงจากไมโครโฟน) เพื่อให้ตัดสินใจได้อย่างแม่นยำและรอบด้าน",
    "points": 1
  },
  {
    "id": "q_fin_20",
    "quiz_uid": 160,
    "chapter_id": "final",
    "category": "final",
    "chapter_number": 0,
    "question_type": "multiple_choice",
    "question_text": "ข้อใดเป็นหลักจริยธรรมและความปลอดภัยที่สำคัญที่สุดในการพัฒนาระบบ Edge AI ที่มีการติดตั้งกล้องและไมโครโฟนในโรงงาน",
    "options": [
      "รักษาความเป็นส่วนตัว (Privacy) โดยประมวลผลข้อมูลที่ตัวอุปกรณ์ ไม่แอบดักฟังเสียงสนทนาส่วนตัว และแจ้งเตือนผู้ปฏิบัติงานอย่างโปร่งใส",
      "แอบบันทึกเสียงบทสนทนาของพนักงานทุกคนเก็บไว้เป็นความลับ",
      "ส่งภาพถ่ายของทุกคนขึ้นสู่โซเชียลมีเดียแบบสาธารณะ",
      "ปิดการทำงานของอุปกรณ์รักษาความปลอดภัยทั้งหมดเพื่อประหยัดไฟ"
    ],
    "correct_index": 0,
    "correct_letter": "ก",
    "explanation": "จริยธรรมด้าน AI กำหนดให้เคารพความเป็นส่วนตัว ซึ่ง Edge AI ตอบโจทย์มากเนื่องจากประมวลผลที่ชิปปลายทางโดยไม่ส่งภาพ/เสียงดิบขึ้นอินเทอร์เน็ต",
    "points": 1
  }
]

def update_databases():
    targets = [
        os.path.join('web_learning_platform', 'data', 'db.json'),
        os.path.join('web_learning_platform', 'data', 'seed.json'),
        os.path.join('web_learning_platform', 'data', 'db.backup.json')
    ]
    
    for target in targets:
        if not os.path.exists(target):
            continue
        with open(target, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        quizzes = data.get('quizzes', [])
        # Keep chapter quizzes (ch01 to ch12, uid 1 to 120)
        chapter_quizzes = [q for q in quizzes if q.get('category') == 'chapter_quiz']
        
        # Merge: chapters 1-12 (120 questions) + midterm (20 questions) + final (20 questions) = 160
        data['quizzes'] = chapter_quizzes + MIDTERM_QUESTIONS + FINAL_QUESTIONS
        
        with open(target, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print(f"[OK] Updated {target} -> Total quizzes: {len(data['quizzes'])}")

def build_midterm_markdown():
    path = "ข้อสอบกลางภาค_ปัญญาประดิษฐ์สมองกลฝังตัว_20ข้อ.md"
    md = []
    md.append("# แบบทดสอบวัดผลการเรียนรู้กลางภาคเรียน (Midterm Examination)")
    md.append("**กลุ่มสาระการเรียนรู้วิทยาศาสตร์และเทคโนโลยี (สาระที่ 4 เทคโนโลยี)**  ")
    md.append("**รายวิชาเพิ่มเติม: ปัญญาประดิษฐ์บนระบบสมองกลฝังตัว (Embedded Artificial Intelligence)**  ")
    md.append("**รหัสวิชา: ว302xx | ระดับชั้นมัธยมศึกษา | เวลาในการทำแบบทดสอบ: 60 นาที | คะแนนเต็ม: 20 คะแนน**  ")
    md.append("**ขอบข่ายเนื้อหา: บทเรียนที่ 1 ถึง บทเรียนที่ 6 (จำนวน 20 ข้อ)**\n")
    md.append("---\n")
    md.append("## ตารางโครงสร้างข้อสอบ (Test Blueprint)\n")
    md.append("| ขอบข่ายเนื้อหาบทเรียน (บทที่ 1–6) | จำนวนข้อ | ข้อที่ | สาระสำคัญที่วัดผล |")
    md.append("| :--- | :---: | :---: | :--- |")
    md.append("| **บทที่ 1: การเตรียมความพร้อมระบบและบอร์ดพัฒนา Arduino UNO Q** | 3 | 1, 2, 3 | สถาปัตยกรรมชิปประมวลผลร่วม, การบูตระบบ, และโหมดเครือข่าย mDNS |")
    md.append("| **บทที่ 2: สถาปัตยกรรมซอฟต์แวร์แบบมอดูล (Modular Brick)** | 3 | 4, 5, 6 | โครงสร้าง Modular Brick, ฟังก์ชัน `App.run()`, และการควบคุม LED Matrix |")
    md.append("| **บทที่ 3: การจัดการระบบฐานข้อมูลด้วย Database-SQL Brick** | 4 | 7, 8, 9, 10 | ฐานข้อมูล SQLite, คำสั่ง CREATE TABLE, INSERT INTO, และการสรุปผล GROUP BY |")
    md.append("| **บทที่ 4: การจัดเตรียมชุดข้อมูลและ Data Pipeline บน Edge Impulse** | 3 | 11, 12, 13 | สัดส่วน Train/Test (80:20), Labeling Method, และผลกระทบขนาดภาพใน Input Block |")
    md.append("| **บทที่ 5: การฝึกสอนโมเดล Visual Anomaly Detection** | 4 | 14, 15, 16 | One-Class Classification, โมเดล FOMO-AD, และการตั้งค่า Anomaly Threshold |")
    md.append("| **บทที่ 6: การนำโมเดล .eim ไปใช้งานและการตั้งค่าไฟล์ app.yaml** | 3 | 17, 18, 19, 20 | โมเดลไบนารี .eim, คำสั่ง `chmod +x`, และไวยากรณ์ `{ ... }` ใน `app.yaml` |")
    md.append("| **รวมทั้งสิ้น** | **20** | **1–20** | **ครอบคลุมสาระสำคัญบทที่ 1 ถึง 6 ครบถ้วน** |\n")
    md.append("---\n")
    md.append("## คำชี้แจงในการทำแบบทดสอบ")
    md.append("1. แบบทดสอบฉบับนี้เป็นแบบทดสอบปรนัย ชนิดเลือกตอบ 4 ตัวเลือก (ก, ข, ค, ง) จำนวน 20 ข้อ ข้อละ 1 คะแนน รวม 20 คะแนน")
    md.append("2. ให้นักเรียนเลือกคำตอบที่ถูกต้องที่สุดเพียงคำตอบเดียว แล้วทำเครื่องหมายกากบาทลงในกระดาษคำตอบ\n")
    md.append("---\n")
    
    for i, q in enumerate(MIDTERM_QUESTIONS, 1):
        md.append(f"#### {i}. {q['question_text']}")
        md.append(f"ก. {q['options'][0]}  ")
        md.append(f"ข. {q['options'][1]}  ")
        md.append(f"ค. {q['options'][2]}  ")
        md.append(f"ง. {q['options'][3]}  \n")
        
    md.append("---\n")
    md.append("## เฉลยคำตอบและคำอธิบายอย่างละเอียด (สำหรับครูผู้สอน)\n")
    for i, q in enumerate(MIDTERM_QUESTIONS, 1):
        md.append(f"{i}. **เฉลย {q['correct_letter']}.**  \n   *คำอธิบาย:* {q['explanation']}\n")
        
    with open(path, 'w', encoding='utf-8') as f:
        f.write("\n".join(md))
    print(f"[OK] Updated {path}")

def build_final_markdown():
    path = "ข้อสอบปลายภาค_ปัญญาประดิษฐ์สมองกลฝังตัว_20ข้อ.md"
    md = []
    md.append("# แบบทดสอบวัดผลการเรียนรู้ปลายภาคเรียน (Final Examination)")
    md.append("**กลุ่มสาระการเรียนรู้วิทยาศาสตร์และเทคโนโลยี (สาระที่ 4 เทคโนโลยี)**  ")
    md.append("**รายวิชาเพิ่มเติม: ปัญญาประดิษฐ์บนระบบสมองกลฝังตัว (Embedded Artificial Intelligence)**  ")
    md.append("**รหัสวิชา: ว302xx | ระดับชั้นมัธยมศึกษา | เวลาในการทำแบบทดสอบ: 60 นาที | คะแนนเต็ม: 20 คะแนน**  ")
    md.append("**ขอบข่ายเนื้อหา: บทเรียนที่ 7 ถึง บทเรียนที่ 12 (จำนวน 20 ข้อ)**\n")
    md.append("---\n")
    md.append("## ตารางโครงสร้างข้อสอบ (Test Blueprint)\n")
    md.append("| ขอบข่ายเนื้อหาบทเรียน (บทที่ 7–12) | จำนวนข้อ | ข้อที่ | สาระสำคัญที่วัดผล |")
    md.append("| :--- | :---: | :---: | :--- |")
    md.append("| **บทที่ 7: การประมวลผล Visual Anomaly และบันทึกลง SQL Brick** | 3 | 1, 2, 3 | กล้อง UVC (/dev/video0), กลไก Debounce, และการบันทึกลง SQLite |")
    md.append("| **บทที่ 8: การฝึกสอนโมเดลตรวจจับวัตถุด้วย FOMO** | 4 | 4, 5, 6, 7 | ความแตกต่างจาก Classification, พิกัด Centroid X, Y, และ Confidence Threshold |")
    md.append("| **บทที่ 9: การนำโมเดล FOMO ไปใช้งานและควบคุม Actuator** | 3 | 8, 9, 10 | ตัวแปร `EI_OBJ_DETECTION_MODEL`, Linear Mapping, และพื้นที่เป้าหมาย (ROI) |")
    md.append("| **บทที่ 10: การพัฒนาโมเดลจำแนกประเภทภาพ (Image Classification)** | 3 | 11, 12, 13 | Transfer Learning (MobileNetV2), คลาส Background, และความหน่วง Latency |")
    md.append("| **บทที่ 11: การประมวลผลสัญญาณเสียงและการฝึกสอน KWS** | 4 | 14, 15, 16, 17 | การแปลง MFCC Spectrogram, ชุดข้อมูล 3 คลาส, และพารามิเตอร์ `debounce_sec` |")
    md.append("| **บทที่ 12: การจำแนกเสียงเฉพาะทางและการบูรณาการ Multi-Modal** | 3 | 18, 19, 20 | Predictive Maintenance, สถาปัตยกรรม Multi-Modal AI, และจริยธรรม Privacy |")
    md.append("| **รวมทั้งสิ้น** | **20** | **1–20** | **ครอบคลุมสาระสำคัญบทที่ 7 ถึง 12 ครบถ้วน** |\n")
    md.append("---\n")
    md.append("## คำชี้แจงในการทำแบบทดสอบ")
    md.append("1. แบบทดสอบฉบับนี้เป็นแบบทดสอบปรนัย ชนิดเลือกตอบ 4 ตัวเลือก (ก, ข, ค, ง) จำนวน 20 ข้อ ข้อละ 1 คะแนน รวม 20 คะแนน")
    md.append("2. ให้นักเรียนเลือกคำตอบที่ถูกต้องที่สุดเพียงคำตอบเดียว แล้วทำเครื่องหมายกากบาทลงในกระดาษคำตอบ\n")
    md.append("---\n")
    
    for i, q in enumerate(FINAL_QUESTIONS, 1):
        md.append(f"#### {i}. {q['question_text']}")
        md.append(f"ก. {q['options'][0]}  ")
        md.append(f"ข. {q['options'][1]}  ")
        md.append(f"ค. {q['options'][2]}  ")
        md.append(f"ง. {q['options'][3]}  \n")
        
    md.append("---\n")
    md.append("## เฉลยคำตอบและคำอธิบายอย่างละเอียด (สำหรับครูผู้สอน)\n")
    for i, q in enumerate(FINAL_QUESTIONS, 1):
        md.append(f"{i}. **เฉลย {q['correct_letter']}.**  \n   *คำอธิบาย:* {q['explanation']}\n")
        
    with open(path, 'w', encoding='utf-8') as f:
        f.write("\n".join(md))
    print(f"[OK] Updated {path}")

if __name__ == '__main__':
    update_databases()
    build_midterm_markdown()
    build_final_markdown()

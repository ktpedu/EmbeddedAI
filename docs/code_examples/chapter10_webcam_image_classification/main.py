#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
รายวิชาเพิ่มเติม: ปัญญาประดิษฐ์บนระบบสมองกลฝังตัว (Embedded Artificial Intelligence)
บทเรียนที่ 10: การเทรนโมเดล AI ให้ใช้กับงาน Image Classification (Brick) ผ่านกล้องเว็ปแคม
สคริปต์: การจำแนกประเภทภาพแบบเวลาจริงผ่านกล้องเว็บแคม และการคัดกรองคลาส Background

คำอธิบาย:
    สคริปต์นี้เรียกใช้งานโมดูล ImageClassification Brick เพื่อรับภาพสดจากกล้องเว็บแคม
    ทำการจำแนกหมวดหมู่วัตถุตามเวลาจริง และคัดกรองไม่ให้ส่งสัญญาณแจ้งเตือนเมื่อระบบตรวจพบ
    คลาสพื้นหลังว่างเปล่า ('background' หรือ 'nothing')
"""

import time
import sys

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

try:
    from arduino.app_bricks.image_classification import ImageClassification
    from arduino.app_utils import App
    IS_ARDUINO_ENV = True
except ImportError:
    IS_ARDUINO_ENV = False

CONFIDENCE_THRESHOLD = 0.80  # เกณฑ์ความเชื่อมั่นขั้นต่ำร้อยละ 80

def handle_classification_result(classification_result):
    """ฟังก์ชัน Callback ตอบสนองผลการจำแนกภาพในแต่ละเฟรม"""
    if not classification_result:
        return
        
    top_label = classification_result.get("label", "Unknown")
    confidence = classification_result.get("confidence", 0.0)
    all_scores = classification_result.get("scores", {})
    
    # 1. คัดกรองคลาสพื้นหลังว่างเปล่า
    if top_label.lower() in ["background", "nothing", "none"]:
        sys.stdout.write(f"\r[-] สถานะ: ฉากหลังว่างเปล่า (Background: {confidence*100:.1f}%)    ")
        sys.stdout.flush()
        return

    # 2. ตรวจสอบเกณฑ์ความเชื่อมั่น
    if confidence >= CONFIDENCE_THRESHOLD:
        print(f"\n[+] [MATCH] จำแนกพบ: '{top_label}' (ความเชื่อมั่น: {confidence*100:.2f}%)")
        print("    -> รายละเอียดคะแนนทุกคลาส:", {k: f"{v*100:.1f}%" for k, v in all_scores.items()})
        
        # ตรรกะควบคุมอุปกรณ์ตามชนิดวัตถุ
        if top_label == "DHT11":
            print("       -> ดำเนินการ: บันทึกข้อมูลคลังเซนเซอร์ DHT11")
        elif top_label == "Tap":
            print("       -> ดำเนินการ: บันทึกข้อมูลคลังข้อต่อวาล์วน้ำ")
    else:
        sys.stdout.write(f"\r[?] ความเชื่อมั่นต่ำ ({top_label}: {confidence*100:.1f}% < {CONFIDENCE_THRESHOLD*100:.0f}%)   ")
        sys.stdout.flush()

def main():
    print("=" * 65)
    print(" ระบบจำแนกประเภทภาพสดผ่านกล้องเว็บแคม (Webcam Image Classification)")
    print("=" * 65)
    
    if not IS_ARDUINO_ENV:
        print("[!] กำลังรันในโหมดจำลอง (Simulated Mode)")
        mock_result_bg = {"label": "background", "confidence": 0.95, "scores": {"background": 0.95, "DHT11": 0.03, "Tap": 0.02}}
        mock_result_tap = {"label": "Tap", "confidence": 0.89, "scores": {"background": 0.04, "DHT11": 0.07, "Tap": 0.89}}
        
        print("\n[*] ทดสอบส่งข้อมูลพื้นหลัง:")
        handle_classification_result(mock_result_bg)
        print("\n[*] ทดสอบส่งข้อมูลตรวจพบวาล์วน้ำ:")
        handle_classification_result(mock_result_tap)
        return

    classifier = ImageClassification()
    classifier.on_classify(handle_classification_result)
    
    print("[*] เริ่มต้นระบบจำแนกภาพแบบเวลาจริง กด Ctrl+C เพื่อออก...")
    App.run()

if __name__ == "__main__":
    main()

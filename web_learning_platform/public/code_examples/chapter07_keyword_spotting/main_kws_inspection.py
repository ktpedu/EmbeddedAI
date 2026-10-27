#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
รายวิชาเพิ่มเติม: ปัญญาประดิษฐ์บนระบบสมองกลฝังตัว (Embedded Artificial Intelligence)
บทเรียนที่ 7: การเทรนโมเดล AI ให้ใช้กับงาน Keyword Spotting (Brick)
สคริปต์: การตรวจสอบคุณลักษณะของโมเดล KWS และลงทะเบียน Callback ตอบสนองคำสั่งเสียง

คำอธิบาย:
    สคริปต์นี้สาธิตการใช้งานคลาส KeywordSpotting เพื่อดึงข้อมูล Metadata (Labels, Sampling Rate)
    และสร้างฟังก์ชัน Callback สำหรับแต่ละป้ายกำกับคำสั่งเสียง (เช่น 'yes', 'no', 'noise', 'unknown')
    ผ่านระบบ Arduino App Lab
"""

import time
import sys

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

try:
    from arduino.app_bricks.keyword_spotting import KeywordSpotting
    from arduino.app_utils import App
    IS_ARDUINO_ENV = True
except ImportError:
    IS_ARDUINO_ENV = False

def setup_keyword_spotter():
    print("=" * 65)
    print(" ระบบตรวจจับคำสั่งเสียงเฉพาะคำ (Keyword Spotting Brick)")
    print("=" * 65)
    
    if not IS_ARDUINO_ENV:
        print("[!] กำลังประมวลผลในโหมดจำลอง (Simulated Mode นอกบอร์ด Arduino UNO Q)")
        mock_labels = ["yes", "no", "noise", "unknown"]
        print(f"[-] รายการคลาสคำสั่งเสียงจำลอง: {mock_labels}")
        for label in mock_labels:
            print(f"    -> [Callback Ready] สำหรับคลาส: '{label}'")
        print("[-] สิ้นสุดการตั้งค่าระบบในโหมดจำลอง")
        return

    # สร้างออบเจ็กต์ KeywordSpotting กำหนด Confidence และ Debounce
    spotter = KeywordSpotting(confidence=0.85, debounce_sec=2.0)
    time.sleep(1.0)  # หน่วงเวลารอการโหลดไฟล์ไบนารี .eim เข้าสู่หน่วยความจำ
    
    info = spotter.get_model_info()
    if info is None:
        print("[!] ข้อผิดพลาด: ไม่สามารถดึงข้อมูล Metadata ของโมเดล KWS ได้")
        print("    กรุณาตรวจสอบว่ามีไฟล์ .eim ใน ei-models และตั้งค่าใน app.yaml ถูกต้องหรือไม่")
        return

    print("=== ข้อมูลแบบจำลอง Keyword Spotting (.eim) ===")
    print(f"[-] ความถี่สุ่มสัญญาณเสียง: {getattr(info, 'frequency', 16000)} Hz")
    print(f"[-] รายชื่อคลาสคำสั่งเสียงทั้งหมด:")
    for label in info.labels:
        print(f"    * {label}")

        # ฟังก์ชัน Factory สำหรับสร้าง Callback แยกตามแต่ละ Label
        def make_callback(detected_label):
            def callback():
                print(f"\n[EVENT] ตรวจพบคำสั่งเสียง: '{detected_label}'")
                if detected_label.lower() == "yes":
                    print("         -> สั่งการ: เปิดระบบไฟฟ้า (Turn ON)")
                elif detected_label.lower() == "no":
                    print("         -> สั่งการ: ปิดระบบไฟฟ้า (Turn OFF)")
                elif detected_label.lower() == "unknown":
                    print("         -> บันทึก: ตรวจพบคำที่ไม่ใช่คำสั่งเป้าหมาย (Ignored)")
            return callback

        spotter.on_detect(label, make_callback(label))

    print("\n[*] เริ่มต้นการดักฟังคำสั่งเสียงผ่านไมโครโฟน (กด Ctrl+C เพื่อหยุดการทำงาน)...")
    App.run()

if __name__ == "__main__":
    setup_keyword_spotter()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
รายวิชาเพิ่มเติม: ปัญญาประดิษฐ์บนระบบสมองกลฝังตัว (Embedded Artificial Intelligence)
บทเรียนที่ 12: การเทรนโมเดล AI ให้ใช้กับงาน Audio Classification (Brick) ผ่านไมโครโฟน
สคริปต์: การดักจับเสียงเหตุการณ์จริงผ่านไมโครโฟน คัดกรองเสียง Background และแจ้งเตือนภัย

คำอธิบาย:
    สคริปต์นี้เรียกใช้งานโมดูล AudioClassification Brick เพื่อเฝ้าระวังเสียงเหตุการณ์สด
    (เช่น เสียงไซเรนเตือนภัย เสียงสัญญาณฉุกเฉิน เสียงสุนัขเห่า หรือเสียงกระจกแตก)
    โดยคัดกรองเสียงบรรยากาศพื้นหลังปกติ ('Background') ออกจากการแจ้งเตือน
    และทำงานร่วมกับระบบบันทึกประวัติเหตุการณ์ (Event Logging System)
"""

import time
import datetime
import sys

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

try:
    from arduino.app_bricks.audio_classification import AudioClassification
    from arduino.app_utils import App
    IS_ARDUINO_ENV = True
except ImportError:
    IS_ARDUINO_ENV = False

CONFIDENCE_THRESHOLD = 0.80  # เกณฑ์ความเชื่อมั่นขั้นต่ำร้อยละ 80

def log_acoustic_event(event_name: str):
    """บันทึกประวัติเหตุการณ์เสียงและสั่งการระบบแจ้งเตือน"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] ตรวจพบเหตุการณ์เสียงฉุกเฉิน: '{event_name}'"
    print(f"\n" + "!" * 65)
    print(f" [ALERT] {log_entry}")
    print("!" * 65)
    print("  -> สั่งการ: ส่งสัญญาณเสียงไซเรนเตือนภัย (Buzzer Alarm Active)")
    print("  -> สั่งการ: บันทึกข้อมูลลงใน Log ไฟล์ /var/log/edge_ai_events.log")
    print("  -> สั่งการ: ส่งรหัสสัญญาณเตือนภัยฉุกเฉินไปยังพยาบาล/เจ้าหน้าที่รักษาความปลอดภัย")

def setup_audio_event_monitoring():
    print("=" * 65)
    print(" ระบบเฝ้าระวังเสียงเหตุการณ์จริงผ่านไมโครโฟน (Audio Event Monitoring)")
    print("=" * 65)
    
    if not IS_ARDUINO_ENV:
        print("[!] กำลังรันในโหมดจำลอง (Simulated Mode นอกบอร์ด UNO Q)")
        print("[*] ทดสอบจำลองการตรวจพบเสียงฉุกเฉิน:")
        log_acoustic_event("Siren_Alarm")
        return

    classifier = AudioClassification(confidence=CONFIDENCE_THRESHOLD)
    time.sleep(1.0)
    
    info = classifier.get_model_info()
    if info is None:
        print("[!] ไม่สามารถดึงข้อมูลแบบจำลองได้ ตรวจสอบไฟล์ app.yaml")
        return

    print("=== ข้อมูลแบบจำลองเสียงเหตุการณ์ ===")
    print(f"[-] รายชื่อคลาสที่รองรับ: {info.labels}")
    
    # ลงทะเบียน Callback เฉพาะคลาสที่ไม่ใช่ Background
    registered_classes = 0
    for label in info.labels:
        if label.lower() != "background":
            registered_classes += 1
            def make_callback(event_label):
                def callback():
                    log_acoustic_event(event_label)
                return callback
            
            classifier.on_detect(label, make_callback(label))
            print(f"    [+] เปิดระบบเฝ้าระวังคลาส: '{label}'")
        else:
            print(f"    [-] ยกเว้นการแจ้งเตือนคลาสพื้นหลัง: '{label}' (Background Filtered)")

    print(f"\n[*] ระบบพร้อมเฝ้าระวังเสียงเหตุการณ์จำนวน {registered_classes} ชนิด กด Ctrl+C เพื่อออก...")
    App.run()

if __name__ == "__main__":
    setup_audio_event_monitoring()

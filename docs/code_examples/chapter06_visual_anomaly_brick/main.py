#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
รายวิชาเพิ่มเติม: ปัญญาประดิษฐ์บนระบบสมองกลฝังตัว (Embedded Artificial Intelligence)
บทเรียนที่ 6: รู้จักกับ “Visual Anomaly Detection Brick” บน Arduino App Lab
สคริปต์: การตรวจสอบความผิดปกติของภาพในโฟลเดอร์ PicsTesting และควบคุมสัญญาณเตือน

คำอธิบาย:
    สคริปต์นี้เป็นชุดคำสั่งหลัก (python/main.py) บน Arduino App Lab ทำหน้าที่เรียกใช้โมดูล
    VisualAnomalyDetection Brick เพื่อวิเคราะห์ภาพชิ้นงานในโฟลเดอร์ ./PicsTesting/
    พร้อมระบบตรวจสอบค่า Anomaly Max Score หากมีค่าเกินเกณฑ์ขีดเริ่มเปลี่ยน (Threshold = 20.0)
    จะสั่งการแจ้งเตือนสถานะความผิดปกติ
"""

import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# นำเข้าโมดูล Visual Anomaly Brick ของระบบ Arduino App Lab
try:
    from arduino.app_bricks.visual_anomaly_detection import VisualAnomalyDetection
    from arduino.app_utils import App
    IS_ARDUINO_ENV = True
except ImportError:
    IS_ARDUINO_ENV = False

ANOMALY_THRESHOLD = 20.0  # เกณฑ์ขีดเริ่มเปลี่ยนสำหรับตัดเกณฑ์ชิ้นงานชำรุด

def process_single_image(vad, image_path: str):
    """วิเคราะห์ความผิดปกติของภาพเดี่ยว"""
    print(f"\n=======================================================")
    print(f"[*] ตรวจสอบไฟล์: {os.path.basename(image_path)}")
    print(f"=======================================================")
    
    if vad is None:
        print("[จำลองระบบ]: รันนอกสภาพแวดล้อม Arduino App Lab")
        return
        
    out = vad.detect_from_file(image_path)
    
    if out and "detection" in out:
        max_score = out.get("anomaly_max_score", 0.0)
        mean_score = out.get("anomaly_mean_score", 0.0)
        
        print(f"[-] คะแนนความผิดปกติสูงสุด (Anomaly Max Score):  {max_score:.2f}")
        print(f"[-] คะแนนความผิดปกติเฉลี่ย (Anomaly Mean Score): {mean_score:.2f}")
        
        # ตรวจสอบว่ามีจุดใดเกินเกณฑ์หรือไม่
        if max_score >= ANOMALY_THRESHOLD:
            print(f"[!] คำเตือน: ตรวจพบชิ้นงานชำรุด/ไม่ได้มาตรฐาน! (Score {max_score:.2f} >= {ANOMALY_THRESHOLD})")
            print("    -> สั่งงาน: เปิดไฟเตือนสีแดง และสั่งคัดแยกชิ้นงาน")
        else:
            print(f"[+] สถานะ: ชิ้นงานปกติสมบูรณ์ ผ่านการตรวจสอบคุณภาพ (Score {max_score:.2f} < {ANOMALY_THRESHOLD})")
            
        print("[-] รายละเอียดพิกัดกรอบที่ตรวจพบความผิดปกติ:")
        for i, anomaly in enumerate(out["detection"]):
            label = anomaly.get("class_name", "Anomaly")
            score = anomaly.get("score", 0.0)
            bbox = anomaly.get("bounding_box_xyxy", [])
            print(f"    {i+1}. {label} | Score: {score:.2f} | Bounding Box [x1,y1,x2,y2]: {bbox}")
    else:
        print("[+] สถานะ: ไม่พบความผิดปกติในภาพ (No anomalies detected - ชิ้นงานสมบูรณ์ 100%)")

def main():
    print("=" * 65)
    print(" โปรแกรมตรวจจับความผิดปกติทางภาพ (Visual Anomaly Detection Brick)")
    print("=" * 65)
    
    testing_folder = "./PicsTesting/"
    
    if IS_ARDUINO_ENV:
        vad = VisualAnomalyDetection()
    else:
        print("[แจ้งเตือน] ไม่พบไลบรารี arduino.app_bricks กำลังทำงานในโหมดจำลอง")
        vad = None
        
    if not os.path.exists(testing_folder):
        print(f"[!] ไม่พบโฟลเดอร์ {testing_folder} กำลังสร้างโฟลเดอร์ตัวอย่าง...")
        os.makedirs(testing_folder, exist_ok=True)
        print(f"    กรุณานำภาพชิ้นงานที่ต้องการทดสอบ (.jpg, .png) มาบันทึกไว้ในโฟลเดอร์ดังกล่าว")
        return
        
    # วนลูปอ่านทุกไฟล์รูปภาพในโฟลเดอร์ทดสอบ
    image_files = [f for f in os.listdir(testing_folder) if f.lower().endswith((".jpg", ".png", ".jpeg"))]
    if not image_files:
        print(f"[*] ไม่พบไฟล์รูปภาพในโฟลเดอร์ {testing_folder}")
        return
        
    print(f"[*] พบไฟล์รูปภาพสำหรับทดสอบจำนวน {len(image_files)} ไฟล์ เริ่มการประมวลผล...")
    for filename in sorted(image_files):
        img_path = os.path.join(testing_folder, filename)
        process_single_image(vad, img_path)

if __name__ == "__main__":
    main()

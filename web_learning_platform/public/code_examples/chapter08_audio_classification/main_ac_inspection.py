#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
รายวิชาเพิ่มเติม: ปัญญาประดิษฐ์บนระบบสมองกลฝังตัว (Embedded Artificial Intelligence)
บทเรียนที่ 8: การเทรนโมเดล AI ให้ใช้กับงาน Audio Classification (Brick)
สคริปต์: การตรวจสอบ Attribute ของโมเดลจำแนกเสียง และการจำแนกประเภทเสียงเหตุการณ์

คำอธิบาย:
    สคริปต์นี้สาธิตการใช้เทคนิค Introspection ในภาษาไพทอน (ฟังก์ชัน dir(), getattr() และ callable())
    เพื่อแยกแยะและตรวจสอบ Metadata ของแบบจำลอง Audio Classification (.eim)
    พร้อมทั้งการเตรียมฟังก์ชันจำแนกเสียงจากไฟล์ทดสอบ (.wav)
"""

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

def inspect_audio_classification_model():
    print("=" * 65)
    print(" การตรวจสอบคุณลักษณะของโมเดล Audio Classification (Introspection)")
    print("=" * 65)
    
    if not IS_ARDUINO_ENV:
        print("[!] กำลังประมวลผลในโหมดจำลอง (Simulated Mode นอกบอร์ด Arduino UNO Q)")
        print("=== ข้อมูลจำลองของคุณลักษณะออบเจ็กต์แบบจำลอง ===")
        print("frequency:   16000")
        print("labels:      ['Background', 'dog_barking', 'glass_breaking']")
        print("model_type:  classification")
        print("interval_ms: 0.0625")
        print("=" * 65)
        return

    classifier = AudioClassification(confidence=0.8)
    info = classifier.get_model_info()
    
    if info is None:
        print("[!] ไม่สามารถดึงข้อมูลโมเดลได้ กรุณาตรวจสอบการตั้งค่า EI_AUDIO_CLASSIFICATION_MODEL ใน app.yaml")
        return

    print("=== รายการ Attributes ทั้งหมดของออบเจ็กต์โมเดล ===")
    for attr in dir(info):
        # คัดกรอง private attribute (นำหน้าด้วย _) และเมธอดที่ callable ออก
        if not attr.startswith("_") and not callable(getattr(info, attr)):
            val = getattr(info, attr)
            print(f"[*] {attr:<18}: {val}")
            
    print("=" * 65)

def classify_audio_file(file_path: str):
    """ฟังก์ชันเสริมสำหรับจำแนกประเภทเสียงจากไฟล์ .wav"""
    if not IS_ARDUINO_ENV:
        print(f"[จำลอง] วิเคราะห์ไฟล์เสียง '{file_path}': ตรวจพบ 'dog_barking' (Confidence: 91.5%)")
        return
        
    classifier = AudioClassification(confidence=0.8)
    result = classifier.classify_from_file(file_path)
    print(f"[*] ผลลัพธ์จากการวิเคราะห์ไฟล์ '{file_path}': {result}")

if __name__ == "__main__":
    inspect_audio_classification_model()
    if len(sys.argv) > 1:
        classify_audio_file(sys.argv[1])

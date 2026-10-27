#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
รายวิชาเพิ่มเติม: ปัญญาประดิษฐ์บนระบบสมองกลฝังตัว (Embedded Artificial Intelligence)
บทเรียนที่ 2: การเทรนโมเดล AI ให้ใช้กับงาน Visual Anomaly Detection (Brick)
สคริปต์: การจำลองการคำนวณและประเมินค่าคะแนนความผิดปกติ (Anomaly Score Processor)

คำอธิบาย:
    สคริปต์นี้สาธิตระเบียบวิธีการประเมินความผิดปกติทางภาพตามหลักการ One-Class Classification
    โดยคำนวณระยะห่างทางสถิติ (Statistical Distance) เทียบกับแบบจำลองการกระจายตัวของชิ้นงานปกติ (Normal Baseline)
    พร้อมทั้งจำลองการตัดสินใจคัดแยกชิ้นงานตามเกณฑ์มาตรฐานทางอุตสาหกรรม
"""

import os
import sys
import math

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def evaluate_anomaly_score(sample_id: str, measured_score: float, threshold: float = 15.0):
    """
    ประเมินและแปลผลค่าคะแนนความผิดปกติ (Anomaly Score)
    
    เกณฑ์มาตรฐาน:
        0 - 5:   ปกติสมบูรณ์ (Normal)
        6 - 15:  ความเปลี่ยนแปลงเล็กน้อย (Minor Variation / Noise)
        > 20:    ตรวจพบความผิดปกติค่อนข้างชัดเจน (Defect Detected)
        > 40:    ตรวจพบความผิดปกติระดับสูงมาก (Critical Defect)
    """
    print(f"\n[*] วิเคราะห์ตัวอย่าง: {sample_id}")
    print(f"    - ค่า Anomaly Score ที่วัดได้: {measured_score:.2f}")
    print(f"    - ค่าขีดเริ่มเปลี่ยน (Threshold): {threshold:.2f}")
    
    if measured_score <= 5.0:
        status = "ผ่านเกณฑ์ (PASS - สมบูรณ์ปกติ)"
        action = "ส่งต่อชิ้นงานเข้าสู่กระบวนการถัดไป"
    elif measured_score <= threshold:
        status = "ผ่านเกณฑ์แบบมีสัญญาณรบกวน (PASS WITH NOISE)"
        action = "บันทึกข้อมูลเพื่อตรวจสอบสภาวะแสง"
    elif measured_score <= 40.0:
        status = "ไม่ผ่านเกณฑ์ (REJECT - พบรอยตำหนิ/ชิ้นส่วนผิดเพี้ยน)"
        action = "สั่งการก้านปัดคัดแยกชิ้นงานชำรุดออกจากสายพาน"
    else:
        status = "ไม่ผ่านเกณฑ์ขั้นวิกฤต (CRITICAL REJECT - ชิ้นงานแตกหัก/ผิดรูปทรงรุนแรง)"
        action = "สั่งการคัดแยกชิ้นงานทันที และส่งสัญญาณเสียงเตือนผู้ควบคุมเครื่องจักร"
        
    print(f"    - ผลการวินิจฉัย: {status}")
    print(f"    - คำสั่งปฏิบัติการ: {action}")
    return measured_score > threshold

def simulate_inspection_batch():
    """จำลองการตรวจสอบชิ้นงานวาล์วน้ำ (Tap) และเซนเซอร์ (DHT11) ในสายการผลิต"""
    print("=" * 70)
    print(" ระบบจำลองการตรวจสอบคุณภาพชิ้นงานด้วย Visual Anomaly Detection")
    print("=" * 70)
    
    test_samples = [
        {"id": "Tap_Sample_01 (วาล์วน้ำสมบูรณ์)", "score": 2.15},
        {"id": "Tap_Sample_02 (วาล์วน้ำมีเงาสะท้อนเล็กน้อย)", "score": 7.80},
        {"id": "Tap_Sample_03 (วาล์วน้ำเกลียวบิ่น)", "score": 24.60},
        {"id": "Tap_Sample_04 (วาล์วน้ำฝาครอบหลุดหาย)", "score": 48.90},
        {"id": "DHT11_Sample_01 (เซนเซอร์สภาพปกติ)", "score": 1.80},
        {"id": "DHT11_Sample_02 (เซนเซอร์ขาตัวนำหักงอ)", "score": 36.40},
    ]
    
    threshold = 15.0
    reject_count = 0
    total_count = len(test_samples)
    
    for sample in test_samples:
        is_reject = evaluate_anomaly_score(sample["id"], sample["score"], threshold)
        if is_reject:
            reject_count += 1
            
    print("\n" + "=" * 70)
    print(f" สรุปผลการตรวจสอบสายการผลิต:")
    print(f" - จำนวนชิ้นงานทั้งหมด: {total_count} ชิ้น")
    print(f" - ผ่านเกณฑ์มาตรฐาน:   {total_count - reject_count} ชิ้น ({((total_count - reject_count)/total_count)*100:.1f}%)")
    print(f" - ชำรุด/คัดแยกออก:     {reject_count} ชิ้น ({(reject_count/total_count)*100:.1f}%)")
    print("=" * 70)

if __name__ == "__main__":
    simulate_inspection_batch()

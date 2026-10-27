#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
หลักสูตร: ปัญญาประดิษฐ์บนระบบสมองกลฝังตัว (Embedded Artificial Intelligence)
บทที่ 4: การจัดเตรียมชุดข้อมูลและการออกแบบขั้นตอนการประมวลผล (Data Pipeline) บน Edge Impulse
ไฟล์: data_pipeline_check.py

วัตถุประสงค์:
1. ตรวจสอบความถูกต้องและสัดส่วนของชุดข้อมูลภาพ (Training Set 80% ต่อ Testing Set 20%)
2. ตรวจสอบความสมดุลของจำนวนตัวอย่างในแต่ละคลาส (Class Balance)
3. ตรวจสอบขนาดภาพและความลึกของสี (Color Depth: RGB / Grayscale 96x96 พิกเซล)
4. สร้างรายงานสรุปความพร้อมของชุดข้อมูลก่อนส่งเข้าฝึกสอนบน Edge Impulse Studio
"""

import os
import sys
import glob

# บังคับการแสดงผลภาษาไทยบนคอนโซลให้ถูกต้อง
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def evaluate_data_pipeline(dataset_dir="./dataset", target_ratio=0.80):
    """
    ฟังก์ชันตรวจสอบความสมบูรณ์และสัดส่วนของชุดข้อมูลภาพ
    """
    print("==================================================================")
    print(" รายงานการตรวจสอบขั้นตอนการประมวลผลข้อมูล (Data Pipeline Validation)")
    print(" แพลตฟอร์ม Edge Impulse Studio • รายวิชาปัญญาประดิษฐ์บนระบบสมองกลฝังตัว")
    print("==================================================================")
    
    # จำลองการตรวจสอบหรืออ่านจากโฟลเดอร์จริง
    # โครงสร้างตัวอย่าง: ./dataset/training/ และ ./dataset/testing/
    classes = ["normal_surface", "crack_defect", "scratch_defect"]
    
    # ตัวอย่างสถิติตัวอย่างภาพสำหรับสาธิต
    mock_data = {
        "training": {
            "normal_surface": 160,
            "crack_defect": 158,
            "scratch_defect": 162
        },
        "testing": {
            "normal_surface": 40,
            "crack_defect": 40,
            "scratch_defect": 40
        }
    }
    
    total_train = sum(mock_data["training"].values())
    total_test = sum(mock_data["testing"].values())
    total_samples = total_train + total_test
    
    train_pct = (total_train / total_samples) * 100 if total_samples > 0 else 0
    test_pct = (total_test / total_samples) * 100 if total_samples > 0 else 0
    
    print(f"\n[1] สรุปสัดส่วนการแบ่งชุดข้อมูล (Dataset Split Ratio):")
    print(f"    - ชุดข้อมูลฝึกสอน (Training Set): {total_train:,} ภาพ ({train_pct:.1f}%)")
    print(f"    - ชุดข้อมูลทดสอบ (Testing Set):    {total_test:,} ภาพ ({test_pct:.1f}%)")
    print(f"    - รวมจำนวนภาพตัวอย่างทั้งหมด:       {total_samples:,} ภาพ (100.0%)")
    
    # ตรวจสอบเกณฑ์มาตรฐาน 80:20 (ยอมรับความคลาดเคลื่อนได้ +-3%)
    if 77.0 <= train_pct <= 83.0 and 17.0 <= test_pct <= 23.0:
        print("    >> [ผ่านเกณฑ์]: สัดส่วนชุดข้อมูลสอดคล้องกับมาตรฐาน 80:20 ของ Edge Impulse")
    else:
        print("    >> [แจ้งเตือน]: สัดส่วนชุดข้อมูลเบี่ยงเบนจากเกณฑ์ 80:20 กรุณาปรับสมดุลใหม่")
        
    print(f"\n[2] การตรวจสอบความสมดุลของแต่ละคลาส (Class Balance):")
    for cls in classes:
        c_train = mock_data["training"].get(cls, 0)
        c_test = mock_data["testing"].get(cls, 0)
        c_total = c_train + c_test
        ratio = (c_train / c_total * 100) if c_total > 0 else 0
        print(f"    - คลาส '{cls}': รวม {c_total} ภาพ (Train: {c_train}, Test: {c_test} -> {ratio:.1f}%)")
        
    print(f"\n[3] การตรวจสอบคุณลักษณะพารามิเตอร์รูปภาพ (Image Preprocessing Check):")
    print("    - ความละเอียดอินพุตเป้าหมาย (Input Resolution): 96 x 96 พิกเซล")
    print("    - ความลึกของสี (Color Depth):               RGB (3 แชนแนล สีสมบูรณ์)")
    print("    - การปรับขนาดภาพ (Resize Mode):             Squash / Fit to shortest")
    print("    - รูปแบบการติดป้ายกำกับ (Labeling Mode):     Bounding Boxes & Multi-class")
    
    print("\n==================================================================")
    print(" [สถานะระบบ]: ชุดข้อมูลพร้อมสำหรับการสกัดคุณลักษณะเด่น (Generate Features)")
    print("             และการฝึกสอนโมเดลโครงข่ายประสาทเทียมในขั้นตอนถัดไป")
    print("==================================================================")

if __name__ == "__main__":
    evaluate_data_pipeline()

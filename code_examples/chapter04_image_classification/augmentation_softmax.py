#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
รายวิชาเพิ่มเติม: ปัญญาประดิษฐ์บนระบบสมองกลฝังตัว (Embedded Artificial Intelligence)
บทเรียนที่ 4: การเทรนโมเดล AI ให้ใช้กับงาน Image Classification (Brick)
สคริปต์: การแปลงค่าความน่าจะเป็น Softmax และหลักการเพิ่มข้อมูลภาพ (Data Augmentation)

คำอธิบาย:
    สคริปต์นี้สาธิตกลไกการคำนวณการกระจายความน่าจะเป็นแบบ Softmax ของโมเดลจำแนกภาพแบบ Multi-class
    (เปรียบเทียบระหว่างคลาส DHT11 และ Tap) และสาธิตพารามิเตอร์การทำ Data Augmentation
    เพื่อป้องกันปัญหา Overfitting ในการฝึกสอนบน Edge Impulse
"""

import math
import sys

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def softmax_probabilities(logits: dict) -> dict:
    """
    คำนวณค่าความน่าจะเป็นด้วยฟังก์ชัน Softmax
    P(y = i | x) = exp(z_i) / sum(exp(z_j))
    """
    labels = list(logits.keys())
    values = list(logits.values())
    
    # ป้องกันภาวะ Numerical Overflow โดยลบด้วยค่าสูงสุด
    max_val = max(values)
    exp_values = [math.exp(v - max_val) for v in values]
    sum_exp = sum(exp_values)
    
    probabilities = {}
    for label, exp_v in zip(labels, exp_values):
        probabilities[label] = exp_v / sum_exp
        
    return probabilities

def classify_sample_with_threshold(probabilities: dict, confidence_threshold: float = 0.70):
    """
    ตัดสินใจจำแนกประเภทภาพตามเกณฑ์ความเชื่อมั่นขั้นต่ำ (Confidence Threshold)
    """
    print("\n" + "-" * 65)
    print(" ผลการคำนวณการกระจายความน่าจะเป็นของภาพ (Classification Probabilities):")
    for label, prob in probabilities.items():
        bar = "█" * int(prob * 30)
        print(f"  [{label:<10}] {prob * 100:6.2f}% | {bar}")
        
    # ค้นหาคลาสที่มีความน่าจะเป็นสูงสุด
    top_label = max(probabilities, key=probabilities.get)
    top_prob = probabilities[top_label]
    
    print("-" * 65)
    if top_prob >= confidence_threshold:
        print(f"[*] ผลการวินิจฉัย: คลาส '{top_label}' (ความเชื่อมั่น: {top_prob * 100:.2f}%) ผ่านเกณฑ์")
    else:
        print(f"[*] ผลการวินิจฉัย: ไม่สามารถระบุคลาสได้อย่างชัดเจน (Uncertain)")
        print(f"    (คะแนนสูงสุด {top_prob * 100:.2f}% ต่ำกว่าเกณฑ์ที่กำหนด {confidence_threshold * 100:.2f}%)")

def display_data_augmentation_config():
    """แสดงพารามิเตอร์มาตรฐานของการเพิ่มความหลากหลายของข้อมูลภาพบน Edge Impulse"""
    print("=" * 65)
    print(" การกำหนดค่า Data Augmentation สำหรับ Transfer Learning (Images)")
    print("=" * 65)
    config = {
        "Random Horizontal Flip": "เปิดใช้งาน (จำลองการกลับด้านวัตถุซ้าย-ขวา)",
        "Random Rotation": "±15 องศา (จำลองการวางเอียงของชิ้นงานบนสายพาน)",
        "Random Brightness": "±20% (จำลองความแปรปรวนของแสงสว่างในแต่ละช่วงเวลา)",
        "Random Zoom / Crop": "0.9x - 1.1x (จำลองระยะห่างระหว่างหน้าเลนส์กับวัตถุ)",
    }
    for k, v in config.items():
        print(f"[*] {k:<26}: {v}")
    print("-> ประโยชน์: ช่วยป้องกันภาวะ Overfitting และเพิ่มความสามารถ Generalization")
    print("=" * 65)

if __name__ == "__main__":
    display_data_augmentation_config()
    
    # ตัวอย่างที่ 1: ผลการประมวลผลที่ตรวจพบวัตถุชัดเจน
    print("\n[กรณีทดสอบที่ 1: ภาพวาล์วน้ำชัดเจน]")
    raw_logits_1 = {"DHT11": 1.2, "Tap": 5.8, "Background": -0.5}
    probs_1 = softmax_probabilities(raw_logits_1)
    classify_sample_with_threshold(probs_1, confidence_threshold=0.80)
    
    # ตัวอย่างที่ 2: ผลการประมวลผลที่ภาพเบลอหรือไม่ชัดเจน
    print("\n[กรณีทดสอบที่ 2: ภาพมีแสงสะท้อนรบกวนมาก]")
    raw_logits_2 = {"DHT11": 2.1, "Tap": 2.3, "Background": 2.0}
    probs_2 = softmax_probabilities(raw_logits_2)
    classify_sample_with_threshold(probs_2, confidence_threshold=0.80)

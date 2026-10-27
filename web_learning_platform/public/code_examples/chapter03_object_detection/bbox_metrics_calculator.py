#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
รายวิชาเพิ่มเติม: ปัญญาประดิษฐ์บนระบบสมองกลฝังตัว (Embedded Artificial Intelligence)
บทเรียนที่ 3: การเทรนโมเดล AI ให้ใช้กับงาน Object Detection (Brick)
สคริปต์: การวิเคราะห์พิกัด Bounding Box และคำนวณตัวชี้วัดประสิทธิภาพ (Metrics Calculator)

คำอธิบาย:
    สคริปต์นี้สาธิตการคำนวณคุณสมบัติทางเรขาคณิตของกรอบวัตถุ (Bounding Box: [xmin, ymin, xmax, ymax])
    การหาจุดศูนย์กลางของวัตถุ (Centroid) ซึ่งเป็นแก่นของแบบจำลอง FOMO
    และการคำนวณค่าตัวชี้วัดความแม่นยำ ได้แก่ Precision, Recall และ F1-Score
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def parse_bounding_box(label: str, bbox: list, confidence: float):
    """
    แยกวิเคราะห์พิกัดกรอบวัตถุและคำนวณจุดศูนย์กลาง (Centroid)
    bbox = [x_min, y_min, x_max, y_max]
    """
    x_min, y_min, x_max, y_max = bbox
    width = x_max - x_min
    height = y_max - y_min
    center_x = (x_min + x_max) / 2.0
    center_y = (y_min + y_max) / 2.0
    
    print(f"[*] วัตถุที่ตรวจพบ: '{label}' (ความเชื่อมั่น: {confidence * 100:.1f}%)")
    print(f"    - พิกัดกรอบมุมซ้ายบน: ({x_min}, {y_min})")
    print(f"    - พิกัดกรอบมุมขวาล่าง: ({x_max}, {y_max})")
    print(f"    - ขนาดมิติของวัตถุ:    ความกว้าง {width} px | ความสูง {height} px")
    print(f"    - จุดกึ่งกลาง (Centroid - FOMO): ({center_x:.1f}, {center_y:.1f})")
    
    return {
        "label": label,
        "width": width,
        "height": height,
        "center": (center_x, center_y),
        "confidence": confidence
    }

def calculate_iou(box_a: list, box_b: list) -> float:
    """คำนวณค่า Intersection over Union (IoU) ระหว่างกรอบจริงและกรอบทำนาย"""
    x_a = max(box_a[0], box_b[0])
    y_a = max(box_a[1], box_b[1])
    x_b = min(box_a[2], box_b[2])
    y_b = min(box_a[3], box_b[3])
    
    inter_area = max(0, x_b - x_a) * max(0, y_b - y_a)
    box_a_area = (box_a[2] - box_a[0]) * (box_a[3] - box_a[1])
    box_b_area = (box_b[2] - box_b[0]) * (box_b[3] - box_b[1])
    union_area = float(box_a_area + box_b_area - inter_area)
    
    return inter_area / union_area if union_area > 0 else 0.0

def calculate_f1_metrics(tp: int, fp: int, fn: int):
    """คำนวณค่า Precision, Recall และ F1-Score"""
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    
    print("\n" + "=" * 65)
    print(" ผลการประเมินประสิทธิภาพของแบบจำลอง Object Detection")
    print("=" * 65)
    print(f"[*] True Positives (TP - ตรวจจับถูกต้อง):   {tp} ชิ้น")
    print(f"[*] False Positives (FP - ตรวจจับผิดพลาด):   {fp} ชิ้น")
    print(f"[*] False Negatives (FN - ตรวจจับตกหล่น):   {fn} ชิ้น")
    print(f"[*] ค่าความแม่นยำ (Precision):               {precision * 100:.2f}%")
    print(f"[*] ค่าความครอบคลุม (Recall):                {recall * 100:.2f}%")
    print(f"[*] ค่าคะแนนฮาร์โมนิก (F1-Score):            {f1 * 100:.2f}%")
    print("=" * 65)

if __name__ == "__main__":
    # ตัวอย่างการวิเคราะห์กรอบวัตถุจริงจากบทเรียน (Tap และ DHT11)
    print("=== ตัวอย่างการวิเคราะห์พิกัดวัตถุในเฟรมภาพ ===")
    sample_bbox = [112, 169, 224, 281]  # อ้างอิงคำถามทบทวนบทเรียนที่ 3
    parse_bounding_box("Tap (วาล์วน้ำ)", sample_bbox, 0.94)
    
    # ตัวอย่างการคำนวณ IoU ระหว่างกรอบเป้าหมายจริงกับกรอบที่โมเดลทาย
    ground_truth = [110, 165, 225, 285]
    predicted = [112, 169, 224, 281]
    iou = calculate_iou(ground_truth, predicted)
    print(f"\n[*] ค่าความทับซ้อน (Intersection over Union: IoU): {iou:.4f} ({iou * 100:.1f}%)")
    
    # คำนวณค่าสถิติ F1-Score สำหรับรายงานผลการทดลอง
    calculate_f1_metrics(tp=48, fp=4, fn=3)

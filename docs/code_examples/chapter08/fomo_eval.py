#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
รายวิชาเพิ่มเติม: ปัญญาประดิษฐ์บนระบบสมองกลฝังตัว (Embedded Artificial Intelligence)
บทเรียนที่ 8: การฝึกสอนโมเดลตรวจจับวัตถุด้วยสถาปัตยกรรม FOMO (Object Detection)
สคริปต์: fomo_eval.py - การประเมินสมรรถนะการตรวจจับวัตถุและคำนวณจุดศูนย์กลาง (Centroid)

คำอธิบาย:
    สคริปต์นี้สาธิตหลักการทำงานของสถาปัตยกรรม FOMO (Faster Objects, More Objects)
    ซึ่งเปลี่ยนปัญหาการตรวจจับวัตถุแบบตีกรอบ (Bounding Box Regression) ให้กลายเป็นการตรวจจับ
    จุดศูนย์กลางของวัตถุบนกริด (Centroid Grid Classification) พร้อมคำนวณตัวชี้วัด
    Precision, Recall, F1-Score และแสดงแผนภาพการกระจายตัวของวัตถุบนตารางจำลอง
"""

import sys
import os
import math

# ตั้งค่าการแสดงผลภาษาไทยบนคอนโซลให้ถูกต้อง
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

GRID_SIZE = 12  # ขนาดกริดคุณลักษณะ (12x12 เซลล์ สำหรับภาพ 96x96 พิกเซล ย่อสเกลละ 8 พิกเซล)
CELL_PIXELS = 8


class FOMOEvaluator:
    """คลาสสำหรับประเมินผลการตรวจจับวัตถุตามสถาปัตยกรรม FOMO"""

    def __init__(self, confidence_threshold: float = 0.60):
        self.confidence_threshold = confidence_threshold
        self.classes = ["bolt", "nut", "bearing"]

    def evaluate_detections(self, detections: list) -> dict:
        """
        ประเมินผลการตรวจจับและนับจำนวนวัตถุ
        
        detections รูปแบบ: [{"label": str, "x": int, "y": int, "width": int, "height": int, "score": float}]
        """
        valid_items = []
        counts = {cls: 0 for cls in self.classes}
        grid_map = [["." for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

        for item in detections:
            score = item.get("score", 0.0)
            if score >= self.confidence_threshold:
                label = item.get("label", "unknown")
                # คำนวณจุดศูนย์กลาง (Centroid)
                cx = item["x"] + item["width"] / 2.0
                cy = item["y"] + item["height"] / 2.0

                # แปลงพิกัดพิกเซลเป็นพิกัดกริด (Grid Cell)
                gx = min(GRID_SIZE - 1, max(0, int(cx // CELL_PIXELS)))
                gy = min(GRID_SIZE - 1, max(0, int(cy // CELL_PIXELS)))

                symbol = label[0].upper()  # B = Bolt, N = Nut, R = Bearing (ลูกปืน)
                if label == "bearing":
                    symbol = "R"
                grid_map[gy][gx] = symbol

                if label in counts:
                    counts[label] += 1

                valid_items.append({
                    "label": label,
                    "centroid_pixel": (round(cx, 1), round(cy, 1)),
                    "grid_coord": (gx, gy),
                    "confidence": round(score, 3)
                })

        return {
            "total_detected": len(valid_items),
            "class_counts": counts,
            "detected_objects": valid_items,
            "grid_map": grid_map
        }

    def print_ascii_grid(self, grid_map: list):
        """แสดงผลแผนภาพตำแหน่งวัตถุบนกริด (Centroid Spatial Map)"""
        print("\n--- แผนภาพแสดงจุดศูนย์กลางของวัตถุบนกริด (Centroid Map 12x12) ---")
        print("    " + " ".join([f"{c:02d}" for c in range(GRID_SIZE)]))
        for r_idx, row in enumerate(grid_map):
            row_str = f"{r_idx:02d} ["
            for char in row:
                if char == "B":
                    row_str += " \033[94mB\033[0m "  # สีน้ำเงิน: Bolt
                elif char == "N":
                    row_str += " \033[93mN\033[0m "  # สีเหลือง: Nut
                elif char == "R":
                    row_str += " \033[92mR\033[0m "  # สีเขียว: Bearing
                else:
                    row_str += " · "
            row_str += "]"
            print(row_str)
        print("    (คำอธิบายสัญลักษณ์: B = น็อตตัวผู้ Bolt, N = น็อตตัวเมีย Nut, R = ตลับลูกปืน Bearing)\n")

    def calculate_metrics(self, tp: int, fp: int, fn: int) -> dict:
        """คำนวณค่า Precision, Recall และ F1-Score"""
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        return {
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1_score": round(f1, 4)
        }


def main():
    print("=" * 75)
    print(" บทเรียนที่ 8: การประเมินสมรรถนะโมเดลตรวจจับวัตถุ FOMO (Object Detection)")
    print(" รายงานการระบุพิกัดจุดศูนย์กลางและจำแนกประเภทชิ้นส่วนอุตสาหกรรม")
    print("=" * 75)

    evaluator = FOMOEvaluator(confidence_threshold=0.60)

    # ชุดข้อมูลจำลองผลการตรวจจับจากกล้องบนสายพานลำเลียง (ภาพขนาด 96x96 พิกเซล)
    mock_detections = [
        {"label": "bolt", "x": 16, "y": 16, "width": 12, "height": 12, "score": 0.88},
        {"label": "bolt", "x": 48, "y": 20, "width": 14, "height": 14, "score": 0.92},
        {"label": "nut", "x": 20, "y": 56, "width": 10, "height": 10, "score": 0.79},
        {"label": "nut", "x": 64, "y": 60, "width": 11, "height": 11, "score": 0.85},
        {"label": "bearing", "x": 36, "y": 40, "width": 24, "height": 24, "score": 0.95},
        {"label": "bolt", "x": 80, "y": 72, "width": 12, "height": 12, "score": 0.52},  # หลุดเกณฑ์ < 0.60
    ]

    results = evaluator.evaluate_detections(mock_detections)

    print(f"[*] เกณฑ์ความเชื่อมั่นขั้นต่ำ (Confidence Threshold): {evaluator.confidence_threshold}")
    print(f"[*] จำนวนวัตถุที่ผ่านเกณฑ์ทั้งหมด: {results['total_detected']} ชิ้น")
    print("\n[*] สรุปจำนวนชิ้นงานจำแนกตามประเภท (Object Counts):")
    for cls, count in results["class_counts"].items():
        print(f"  ├─ {cls.capitalize():<12} : {count} ชิ้น")

    print("\n[*] รายละเอียดพิกัดจุดศูนย์กลางของวัตถุ (Detected Objects):")
    for idx, obj in enumerate(results["detected_objects"], 1):
        print(f"  [{idx:02d}] {obj['label'].upper():<8} | พิกัดพิกเซล: {obj['centroid_pixel']} | พิกัดกริด: {obj['grid_coord']} | Conf: {obj['confidence']}")

    evaluator.print_ascii_grid(results["grid_map"])

    # จำลองการคำนวณตัวชี้วัดประสิทธิภาพของโมเดลในการทดสอบรวม (Confusion Metrics)
    print("=" * 75)
    print(" รายงานตัวชี้วัดประสิทธิภาพเชิงสถิติ (Model Evaluation Metrics)")
    print("=" * 75)
    metrics_data = [
        ("Bolt (น็อตตัวผู้)", 45, 3, 2),
        ("Nut (น็อตตัวเมีย)", 40, 2, 4),
        ("Bearing (ตลับลูกปืน)", 50, 1, 1),
    ]

    print(f"{'คลาสวัตถุ':<22} | {'TP':<4} | {'FP':<4} | {'FN':<4} | {'Precision':<10} | {'Recall':<8} | {'F1-Score':<8}")
    print("-" * 75)
    for name, tp, fp, fn in metrics_data:
        m = evaluator.calculate_metrics(tp, fp, fn)
        print(f"{name:<22} | {tp:<4} | {fp:<4} | {fn:<4} | {m['precision']:<10} | {m['recall']:<8} | {m['f1_score']:<8}")
    print("-" * 75)
    print("[สรุปผล] สถาปัตยกรรม FOMO ให้ค่า F1-Score สูงกว่า 94% บนขนาดโมเดลที่กะทัดรัดยิ่งยวด\n")


if __name__ == "__main__":
    main()

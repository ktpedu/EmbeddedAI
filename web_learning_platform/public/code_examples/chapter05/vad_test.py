#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
รายวิชาเพิ่มเติม: ปัญญาประดิษฐ์บนระบบสมองกลฝังตัว (Embedded Artificial Intelligence)
บทเรียนที่ 5: การฝึกสอนโมเดลตรวจจับความผิดปกติจากภาพ (Visual Anomaly Detection)
สคริปต์: vad_test.py - การทดสอบและประเมินผลค่าคะแนนความผิดปกติ (Anomaly Score Evaluator)

คำอธิบาย:
    สคริปต์นี้สาธิตระเบียบวิธีการประมวลผลและตัดสินผลการตรวจจับความผิดปกติทางสายตา (Visual Anomaly Detection)
    ตามหลักการ One-Class Learning โดยอาศัยโครงข่ายประสาทเทียมสกัดคุณลักษณะเด่น (Feature Extractor)
    และการคำนวณระยะห่างทางสถิติของเวกเตอร์คุณลักษณะ (Feature Vector Distance) เทียบกับแบบจำลองชิ้นงานปกติ
    พร้อมทั้งแสดงการวิเคราะห์ค่าคะแนนเฉลี่ย (Mean Score), ค่าคะแนนสูงสุด (Max Score) และตำแหน่งกริดที่มีรอยตำหนิ
"""

import sys
import os
import json
import random

# ตั้งค่าการแสดงผลภาษาไทยบนคอนโซลให้ถูกต้อง
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

class VisualAnomalyEvaluator:
    """คลาสสำหรับประเมินและตัดสินผลการตรวจจับความผิดปกติจากภาพ"""

    def __init__(self, threshold: float = 20.0, critical_threshold: float = 40.0, grid_size: int = 12):
        self.threshold = threshold
        self.critical_threshold = critical_threshold
        self.grid_size = grid_size  # ขนาดกริดคุณลักษณะ เช่น 12x12 ช่องย่อย

    def evaluate_sample(self, sample_name: str, grid_scores: list) -> dict:
        """
        คำนวณค่าคะแนนความผิดปกติจากชุดข้อมูลกริดของภาพ
        
        พารามิเตอร์:
            sample_name (str): ชื่อหรือรหัสประจำตัวของชิ้นงานตัวอย่าง
            grid_scores (list of list of float): แมทริกซ์ค่าคะแนนความผิดปกติระดับกริด (Grid Map)
            
        คืนค่า:
            dict: พจนานุกรมผลลัพธ์การประเมิน
        """
        flat_scores = [score for row in grid_scores for score in row]
        mean_score = sum(flat_scores) / len(flat_scores)
        max_score = max(flat_scores)
        
        # ค้นหาพิกัดกริดที่พบค่าคะแนนความผิดปกติสูงสุด
        max_pos = (0, 0)
        for r_idx, row in enumerate(grid_scores):
            for c_idx, val in enumerate(row):
                if val == max_score:
                    max_pos = (r_idx, c_idx)
                    break

        # ตัดสินผลตามเกณฑ์ขีดเริ่มเปลี่ยน (Thresholding Logic)
        if max_score > self.critical_threshold:
            verdict = "REJECT_CRITICAL"
            status_desc = "ไม่ผ่านเกณฑ์ขั้นวิกฤต (พบการชำรุดรุนแรง/แตกหัก)"
            action_desc = "สั่งการก้านปัดคัดแยกชิ้นงาน และส่งสัญญาณแจ้งเตือนผู้ควบคุมเครื่องจักร"
        elif max_score > self.threshold:
            verdict = "REJECT_DEFECT"
            status_desc = "ไม่ผ่านเกณฑ์ (ตรวจพบรอยตำหนิ/รอยขีดข่วนผิดปกติ)"
            action_desc = "สั่งการก้านปัดคัดแยกชิ้นงานออกสู่ช่องกักกันเพื่อตรวจสอบซ้ำ"
        elif max_score > (self.threshold * 0.6):
            verdict = "PASS_WARNING"
            status_desc = "ผ่านเกณฑ์แบบเฝ้าระวัง (มีความผันแปรของแสงหรือพื้นผิวเล็กน้อย)"
            action_desc = "ส่งต่อชิ้นงานเข้าสู่กระบวนการถัดไป พร้อมบันทึกภาพลงฐานข้อมูลเพื่อวิเคราะห์แนวโน้ม"
        else:
            verdict = "PASS_NORMAL"
            status_desc = "ผ่านเกณฑ์มาตรฐานสมบูรณ์ (ชิ้นงานปกติ)"
            action_desc = "ส่งต่อชิ้นงานเข้าสู่กระบวนการบรรจุภัณฑ์ถัดไป"

        return {
            "sample_name": sample_name,
            "mean_score": round(mean_score, 2),
            "max_score": round(max_score, 2),
            "defect_coordinate": max_pos,
            "threshold": self.threshold,
            "verdict": verdict,
            "status_description": status_desc,
            "recommended_action": action_desc
        }

    def print_grid_heatmap(self, grid_scores: list, sample_name: str):
        """แสดงผลแผนภาพความร้อนแบบตัวอักษร (ASCII Heatmap) จำลองตำแหน่งความผิดปกติ"""
        print(f"\n--- แผนภาพความผิดปกติ (Feature Grid Heatmap): {sample_name} ---")
        print("    " + " ".join([f"{c:02d}" for c in range(len(grid_scores[0]))]))
        for r_idx, row in enumerate(grid_scores):
            row_str = f"{r_idx:02d} ["
            for val in row:
                if val >= self.threshold:
                    row_str += " \033[91m##\033[0m"  # สีแดง: เกินเกณฑ์ผิดปกติ
                elif val >= self.threshold * 0.6:
                    row_str += " \033[93m··\033[0m"  # สีเหลือง: ระดับเฝ้าระวัง
                else:
                    row_str += "   "  # ช่องว่าง: ปกติ
            row_str += " ]"
            print(row_str)


def generate_mock_grid(condition: str = "normal", grid_dim: int = 12) -> list:
    """ฟังก์ชันสร้างข้อมูลกริดคะแนนจำลองเพื่อใช้ทดสอบระบบ"""
    grid = []
    for _ in range(grid_dim):
        row = [round(random.uniform(0.5, 4.0), 2) for _ in range(grid_dim)]
        grid.append(row)
        
    if condition == "minor_scratch":
        # จำลองรอยขีดข่วนขนาดเล็ก 2 ช่อง
        grid[4][5] = 23.5
        grid[4][6] = 21.8
    elif condition == "critical_crack":
        # จำลองรอยแตกหักขนาดใหญ่
        for offset in range(3):
            grid[7 + offset][8] = 45.2 + offset * 2.1
            grid[7 + offset][9] = 42.0 + offset * 1.5
    elif condition == "surface_noise":
        # จำลองแสงสะท้อนหรือฝุ่นละอองบางๆ
        grid[2][3] = 13.4
        grid[2][4] = 14.1

    return grid


def main():
    print("=" * 75)
    print(" บทเรียนที่ 5: โครงการตรวจจับความผิดปกติจากภาพบนระบบสมองกลฝังตัว (FOMO-AD)")
    print(" รายงานผลการประเมินคะแนนความผิดปกติ (Visual Anomaly Assessment)")
    print("=" * 75)

    evaluator = VisualAnomalyEvaluator(threshold=20.0, critical_threshold=40.0, grid_size=12)

    # ชุดข้อมูลจำลองสำหรับการทดสอบ 4 กรณี
    test_cases = [
        ("BEARING_SAMPLE_001 (ลูกปืนปกติสมบูรณ์)", "normal"),
        ("BEARING_SAMPLE_002 (ลูกปืนมีแสงสะท้อนผิวด้าน)", "surface_noise"),
        ("BEARING_SAMPLE_003 (ลูกปืนมีรอยตามด/รอยขีดข่วน)", "minor_scratch"),
        ("BEARING_SAMPLE_004 (ลูกปืนแตกร้าวรุนแรง)", "critical_crack"),
    ]

    summary_results = []

    for name, condition in test_cases:
        grid_data = generate_mock_grid(condition=condition, grid_dim=12)
        result = evaluator.evaluate_sample(sample_name=name, grid_scores=grid_data)
        summary_results.append(result)

        print(f"\n[การประเมิน] {result['sample_name']}")
        print(f"  ├─ คะแนนเฉลี่ย (Mean Score):     {result['mean_score']}")
        print(f"  ├─ คะแนนสูงสุด (Max Score):      {result['max_score']}")
        print(f"  ├─ พิกัดกริดที่ตรวจพบ (Row, Col):  {result['defect_coordinate']}")
        print(f"  ├─ ผลการวินิจฉัย (Verdict):       {result['status_description']}")
        print(f"  └─ คำสั่งปฏิบัติการทางกายภาพ:     {result['recommended_action']}")

        if result['verdict'] in ["REJECT_DEFECT", "REJECT_CRITICAL"]:
            evaluator.print_grid_heatmap(grid_data, name)

    print("\n" + "=" * 75)
    print(" สรุปผลการทดสอบการตรวจสอบคุณภาพชิ้นงานเชิงสถิติ")
    print("=" * 75)
    print(f"{'รหัสชิ้นงาน':<35} | {'Mean':<6} | {'Max':<6} | {'สถานะ':<15}")
    print("-" * 75)
    for res in summary_results:
        code_short = res['sample_name'].split()[0]
        status_short = "ผ่าน (PASS)" if "PASS" in res['verdict'] else "ปฏิเสธ (REJECT)"
        print(f"{code_short:<35} | {res['mean_score']:<6} | {res['max_score']:<6} | {status_short:<15}")
    print("-" * 75)
    print("[เสร็จสิ้น] ระบบประเมินค่าคะแนนความผิดปกติพร้อมนำไปเชื่อมโยงร่วมกับ Modular Brick\n")


if __name__ == "__main__":
    main()

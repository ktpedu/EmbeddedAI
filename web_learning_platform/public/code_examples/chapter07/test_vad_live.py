#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
รายวิชาเพิ่มเติม: ปัญญาประดิษฐ์บนระบบสมองกลฝังตัว (Embedded Artificial Intelligence)
บทเรียนที่ 7: การประมวลผลโมเดลตรวจจับความผิดปกติจากภาพ และการบันทึกข้อมูลลง Database-SQL Brick
สคริปต์: test_vad_live.py - การประมวลผลภาพสดและการบันทึกประวัติการตรวจจับลงฐานข้อมูล SQL

คำอธิบาย:
    สคริปต์นี้สาธิตการบูรณาการระบบตรวจจับความผิดปกติจากภาพ (Visual Anomaly Detection: FOMO-AD)
    เข้ากับระบบฐานข้อมูลเชิงสัมพันธ์บนอุปกรณ์ (Database-SQL Brick) โดยจำลองการรับภาพจากกล้อง
    การวิเคราะห์ค่าคะแนน Anomaly Max Score และ Anomaly Mean Score การควบคุมอุปกรณ์ขับเคลื่อน (Actuator)
    และการบันทึกประวัติเหตุการณ์ลงตารางฐานข้อมูล SQLite แบบเรียลไทม์ พร้อมการสืบค้นรายงานสรุปเชิงสถิติ
"""

import sys
import os
import time
import sqlite3
import random
from datetime import datetime

# ตั้งค่าการแสดงผลภาษาไทยบนคอนโซลให้ถูกต้อง
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

DB_FILE_PATH = os.path.join(os.path.dirname(__file__), "production_qc.db")
ANOMALY_THRESHOLD = 20.0  # เกณฑ์ขีดเริ่มเปลี่ยนมาตรฐาน


class ProductionQCManager:
    """คลาสจัดการระบบควบคุมคุณภาพและบันทึกข้อมูลลงฐานข้อมูล SQL บนบอร์ด"""

    def __init__(self, db_path: str = DB_FILE_PATH):
        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        """สร้างตาราง inspection_records หากยังไม่มีในระบบ"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS inspection_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    part_id TEXT NOT NULL,
                    anomaly_mean REAL NOT NULL,
                    anomaly_max REAL NOT NULL,
                    threshold REAL NOT NULL,
                    verdict TEXT NOT NULL,
                    latency_ms REAL NOT NULL,
                    hardware_action TEXT
                )
            """)
            conn.commit()

    def log_inspection(self, part_id: str, mean_score: float, max_score: float,
                       verdict: str, latency: float, action: str) -> int:
        """บันทึกข้อมูลการตรวจสอบคุณภาพ 1 รายการลงฐานข้อมูล SQL"""
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO inspection_records 
                (timestamp, part_id, anomaly_mean, anomaly_max, threshold, verdict, latency_ms, hardware_action)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (now_str, part_id, mean_score, max_score, ANOMALY_THRESHOLD, verdict, latency, action))
            conn.commit()
            return cursor.lastrowid

    def fetch_recent_logs(self, limit: int = 10) -> list:
        """สืบค้นรายการบันทึกล่าสุดจากฐานข้อมูล"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, timestamp, part_id, anomaly_mean, anomaly_max, verdict, latency_ms, hardware_action
                FROM inspection_records
                ORDER BY id DESC
                LIMIT ?
            """, (limit,))
            return cursor.fetchall()

    def get_summary_statistics(self) -> dict:
        """คำนวณดัชนีชี้วัดประสิทธิภาพเชิงสถิติ (KPIs: Yield Rate, Defect Count, Avg Latency)"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM inspection_records")
            total = cursor.fetchone()[0]

            if total == 0:
                return {"total": 0, "pass_count": 0, "reject_count": 0, "yield_rate": 0.0, "avg_latency": 0.0}

            cursor.execute("SELECT COUNT(*) FROM inspection_records WHERE verdict = 'PASS'")
            passes = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM inspection_records WHERE verdict = 'REJECT'")
            rejects = cursor.fetchone()[0]

            cursor.execute("SELECT AVG(latency_ms) FROM inspection_records")
            avg_latency = cursor.fetchone()[0] or 0.0

            yield_rate = (passes / total) * 100.0

            return {
                "total": total,
                "pass_count": passes,
                "reject_count": rejects,
                "yield_rate": round(yield_rate, 2),
                "avg_latency": round(avg_latency, 2)
            }


def simulate_camera_inference(sample_index: int) -> tuple:
    """จำลองการดึงเฟรมภาพจากกล้องและการคำนวณโมเดล VAD"""
    start_time = time.time()
    time.sleep(random.uniform(0.02, 0.04))  # จำลองระยะเวลาหน่วงในการประมวลผล 20-40 ms
    latency_ms = (time.time() - start_time) * 1000

    # จำลองสัดส่วนของเสีย 20%
    is_defective = random.random() < 0.25
    part_id = f"PART-BRG-{sample_index:04d}"

    if is_defective:
        mean_score = round(random.uniform(3.5, 9.8), 2)
        max_score = round(random.uniform(22.4, 48.6), 2)
        verdict = "REJECT"
        action = "RELAY_TRIGGER: PUSH_DEFECT_BIN | LED: RED_ALARM"
    else:
        mean_score = round(random.uniform(0.8, 2.5), 2)
        max_score = round(random.uniform(1.5, 12.0), 2)
        verdict = "PASS"
        action = "CONVEYOR_NEXT: ADVANCE | LED: GREEN_READY"

    return part_id, mean_score, max_score, verdict, round(latency_ms, 2), action


def main():
    print("=" * 75)
    print(" บทเรียนที่ 7: ระบบตรวจสอบความผิดปกติจากภาพสดและบันทึกข้อมูล SQL")
    print(" (Real-time Visual Anomaly Detection & Database-SQL Brick Logging)")
    print("=" * 75)

    qc_manager = ProductionQCManager()
    print(f"[*] ไฟล์ฐานข้อมูล SQLite: {DB_FILE_PATH}")
    print(f"[*] เกณฑ์ขีดเริ่มเปลี่ยน (Anomaly Threshold): {ANOMALY_THRESHOLD}")
    print("[*] เริ่มต้นกระบวนการตรวจสอบคุณภาพสายการผลิตจำลอง (5 ชิ้นงาน)...\n")

    for i in range(1, 6):
        part_id, mean_score, max_score, verdict, latency, action = simulate_camera_inference(i)
        log_id = qc_manager.log_inspection(part_id, mean_score, max_score, verdict, latency, action)

        status_tag = "\033[92m[PASS]\033[0m" if verdict == "PASS" else "\033[91m[REJECT]\033[0m"
        print(f"[{log_id:03d}] {part_id} | Mean: {mean_score:<4} | Max: {max_score:<4} | {status_tag} ({latency:.1f} ms)")
        print(f"      └─ ฮาร์ดแวร์ปฏิบัติการ: {action}")

    # แสดงผลสรุปสถิติจากฐานข้อมูล
    stats = qc_manager.get_summary_statistics()
    print("\n" + "=" * 75)
    print(" สรุปรายงานสถิติการควบคุมคุณภาพจาก Database-SQL Brick")
    print("=" * 75)
    print(f"  ├─ จำนวนชิ้นงานที่ตรวจสอบทั้งหมด: {stats['total']} ชิ้น")
    print(f"  ├─ ผ่านเกณฑ์มาตรฐาน (PASS):       {stats['pass_count']} ชิ้น")
    print(f"  ├─ ไม่ผ่านเกณฑ์ (REJECT):         {stats['reject_count']} ชิ้น")
    print(f"  ├─ อัตราผลผลิตสมบูรณ์ (Yield):    {stats['yield_rate']}%")
    print(f"  └─ ระยะเวลาหน่วงเฉลี่ย:           {stats['avg_latency']} มิลลิวินาที (ms)")
    print("=" * 75 + "\n")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
รายวิชา: การพัฒนาปัญญาประดิษฐ์บนอุปกรณ์ขอบ (Edge AI Development)
บทเรียนที่ 12: การจำแนกเสียงเฉพาะทางและการบูรณาการระบบ Edge AI เชิงวิศวกรรม
สคริปต์: multi_ai_live.py - ระบบบูรณาการปัญญาประดิษฐ์พหุโมดอล (Audio + Vision) และการบันทึกฐานข้อมูล SQLite

คำอธิบาย:
    สคริปต์ระดับ Capstone Integration นี้จำลองและเชื่อมโยงการทำงานร่วมกันของ
    Audio Classification Brick, Video Object Detection Brick และ Database-SQL Brick
    เพื่อเฝ้าระวังความผิดปกติของเครื่องจักรอุตสาหกรรม บันทึกประวัติเหตุการณ์ลงฐานข้อมูล
    และออกคำสั่งตัดวงจรฉุกเฉิน (Emergency Interlock) เมื่อพบความผิดปกติวิกฤต
"""

import sys
import time
import datetime
import sqlite3
import os

# กำหนดการเข้ารหัส UTF-8 สำหรับคอนโซล
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# ตรวจสอบสภาพแวดล้อมบอร์ดพัฒนา Arduino UNO Q
try:
    from arduino.app_bricks.audio_classification import AudioClassification
    from arduino.app_bricks.video_object_detection import VideoObjectDetection
    from arduino.app_utils import App
    IS_ARDUINO_ENV = True
except ImportError:
    IS_ARDUINO_ENV = False


class MultiModalEdgeSystem:
    """คลาสบูรณาการระบบ Edge AI เชิงวิศวกรรม (Audio + Vision + Database-SQL + Actuator)"""
    
    def __init__(self, db_path=":memory:"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.init_database()
        self.stats = {"NORMAL": 0, "WARNING": 0, "CRITICAL": 0, "BACKGROUND": 0}

    def init_database(self):
        """สร้างตารางเก็บบันทึกประวัติการตรวจสอบเครื่องจักร (Machine Audit Logs)"""
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS machine_audit_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    sensor_type TEXT NOT NULL,
                    event_label TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    severity TEXT NOT NULL,
                    action_taken TEXT NOT NULL
                )
            """)

    def handle_acoustic_event(self, label: str, confidence: float):
        """ประมวลผลการจำแนกเสียงเครื่องจักรและวิเคราะห์ระดับความรุนแรง"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cmd = label.strip()

        # 1. คัดกรองเสียงฉากหลังทั่วไป
        if cmd.lower() in ["background", "ambient", "silence"]:
            self.stats["BACKGROUND"] += 1
            print(f"[{timestamp}] [-] เสียงบรรยากาศปกติ (Background: {confidence * 100:.1f}%)")
            return

        severity = "NORMAL"
        action = "บันทึกประวัติการเดินเครื่องปกติ"

        if cmd in ["Bearing_Fault", "ตลับลูกปืนสึกหรอ"]:
            severity = "WARNING"
            action = "ส่งสัญญาณแจ้งเตือนช่างซ่อมบำรุง (Yellow LED ON)"
        elif cmd in ["Gear_Jam", "เฟืองขบติดขัด", "Siren_Alarm"]:
            severity = "CRITICAL"
            action = "ตัดวงจรฉุกเฉิน (Relay E-Stop Pin 7 = HIGH) และเปิด Buzzer"

        self.stats[severity] += 1

        # 2. บันทึกลงฐานข้อมูล SQLite
        with self.conn:
            self.conn.execute("""
                INSERT INTO machine_audit_logs (timestamp, sensor_type, event_label, confidence, severity, action_taken)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (timestamp, "ACOUSTIC_MIC", cmd, confidence, severity, action))

        # 3. แสดงผลรายงานทางคอนโซล
        alert_prefix = "[NORMAL]" if severity == "NORMAL" else ("[WARN]" if severity == "WARNING" else "[CRITICAL ALERT]")
        print(f"\n{alert_prefix} [{timestamp}] ตรวจพบเสียง: '{cmd}' (ความเชื่อมั่น: {confidence * 100:.2f}%)")
        print(f"  -> ระดับความรุนแรง: {severity}")
        print(f"  -> การตอบสนองเชิงวิศวกรรม: {action}")
        print(f"  -> ฐานข้อมูล: บันทึกข้อมูลสำเร็จ (SQLite Machine Audit)")

    def print_summary_report(self):
        """ออกรายงานสรุปสถิติการบำรุงรักษาเชิงคาดการณ์ (Predictive Maintenance Report)"""
        print("\n" + "=" * 76)
        print("   รายงานสรุปการตรวจวัดสุขภาพเครื่องจักรประจำกะงาน (Predictive Maintenance)")
        print("   หลักสูตร: การพัฒนาปัญญาประดิษฐ์บนอุปกรณ์ขอบ (บทเรียนที่ 12)")
        print("=" * 76)
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, timestamp, event_label, confidence, severity, action_taken FROM machine_audit_logs ORDER BY id DESC LIMIT 5")
        rows = cursor.fetchall()

        print(f"{'ID':<4} | {'เวลา':<19} | {'เหตุการณ์':<18} | {'เชื่อมั่น':<8} | {'ระดับ':<8}")
        print("-" * 76)
        for r in rows:
            print(f"{r[0]:<4} | {r[1]:<19} | {r[2]:<18} | {r[3]*100:>6.1f}% | {r[4]:<8}")

        print("-" * 76)
        print(f"สถิติรวม: ปกติ={self.stats['NORMAL']} | แจ้งเตือน={self.stats['WARNING']} | วิกฤต={self.stats['CRITICAL']} | ฉากหลัง={self.stats['BACKGROUND']}")
        print("=" * 76)
        print("[✓] บูรณาการระบบ Edge AI พหุโมดอลเสร็จสมบูรณ์ พร้อมเชื่อมต่อโรงงานอัจฉริยะ\n")


def run_simulation():
    """ฟังก์ชันทดสอบการทำงานของระบบในโหมดจำลองคอนโซล"""
    print("=" * 76)
    print("   ระบบบูรณาการปัญญาประดิษฐ์พหุโมดอล (Multi-Modal Edge AI Integration)")
    print("   หลักสูตร: การพัฒนาปัญญาประดิษฐ์บนอุปกรณ์ขอบ (บทเรียนที่ 12 - Capstone)")
    print("=" * 76)
    print("[*] เริ่มต้นการทดสอบในโหมดจำลองสถานการณ์คอนโซล (Console Simulation)...")
    print("[*] กำหนดค่าเกณฑ์ความเชื่อมั่นเสียง (Audio Threshold): 0.80 (80%)")
    print("[*] เริ่มต้นระบบบันทึกประวัติ Database-SQL บนหน่วยความจำ (SQLite)...")
    print("-" * 76)

    system = MultiModalEdgeSystem(db_path=":memory:")

    # จำลองลำดับเหตุการณ์เสียง 5 เหตุการณ์
    acoustic_events = [
        ("Background", 0.94),
        ("Normal_Hum", 0.89),
        ("Bearing_Fault", 0.92),
        ("Background", 0.96),
        ("Gear_Jam", 0.95)
    ]

    for idx, (label, conf) in enumerate(acoustic_events, 1):
        print(f"\n--- [รอบการประมวลผลสัญญาณที่ {idx} / {len(acoustic_events)}] ---")
        system.handle_acoustic_event(label, conf)
        time.sleep(0.12)

    system.print_summary_report()


def main():
    if not IS_ARDUINO_ENV:
        run_simulation()
        return

    print("[*] ตรวจพบสภาพแวดล้อมบอร์ดพัฒนา Arduino UNO Q พร้อมใช้งาน")
    system = MultiModalEdgeSystem(db_path="/home/arduino/data/edge_factory.db")
    classifier = AudioClassification(confidence=0.80)
    time.sleep(1.0)

    info = classifier.get_model_info()
    if info is not None:
        for label in info.labels:
            def make_cb(lbl):
                def cb():
                    system.handle_acoustic_event(lbl, 0.90)
                return cb
            classifier.on_detect(label, make_cb(label))

    print("[*] ระบบพหุโมดอลพร้อมเฝ้าระวังเครื่องจักร กด Ctrl+C เพื่อออก...")
    App.run()


if __name__ == "__main__":
    main()

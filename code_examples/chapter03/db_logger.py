#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ระบบจัดการฐานข้อมูล SQL บนบอร์ด Arduino UNO Q (Database-SQL Brick)
อ้างอิงคลิป Arduino UNO Q รู้จักกับ "Database-SQL Brick" บน Arduino App Lab

ทำหน้าที่:
1. สร้างฐานข้อมูล SQLite ในเครื่อง (/home/arduino/.arduino-bricks/data/edgeai_records.db)
2. สร้างตารางบันทึกผลการตรวจจับ AI (ai_inference_logs)
3. บันทึกผลการทำนายโมเดล (Inference Logging): Anomaly Score, FOMO Object Coordinates, KWS Commands
4. ดึงรายงานสถิติย้อนหลัง (Query Summary) สำหรับระบบอุตสาหกรรมอัตโนมัติ
"""

import os
import sys
import sqlite3
import datetime

# บังคับการแสดงผลภาษาไทยบนคอนโซลให้ถูกต้อง
if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')

# กำหนดพาธฐานข้อมูลตามคอนฟิกูเรชัน app.yaml
DB_PATH = os.environ.get("DB_FILE_PATH", "edgeai_records.db")

def init_database():
    """สร้างตารางในฐานข้อมูลหากยังไม่มี"""
    os.makedirs(os.path.dirname(os.path.abspath(DB_PATH)), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. ตารางบันทึกประวัติการตรวจจับความผิดปกติ (Visual Anomaly Detection)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS anomaly_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            model_name TEXT NOT NULL,
            anomaly_mean_score REAL,
            anomaly_max_score REAL,
            status TEXT NOT NULL,
            alert_triggered INTEGER DEFAULT 0
        )
    ''')
    
    # 2. ตารางบันทึกประวัติการตรวจจับวัตถุ (FOMO Object Detection)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS object_detection_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            label TEXT NOT NULL,
            confidence REAL NOT NULL,
            pos_x INTEGER NOT NULL,
            pos_y INTEGER NOT NULL,
            width INTEGER,
            height INTEGER
        )
    ''')

    # 3. ตารางบันทึกประวัติคำสั่งเสียง (Keyword Spotting)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS kws_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            keyword TEXT NOT NULL,
            confidence REAL NOT NULL,
            action_executed TEXT
        )
    ''')

    conn.commit()
    conn.close()
    print(f"[Database-SQL Brick] เริ่มต้นโครงสร้างตารางฐานข้อมูลสำเร็จ: {DB_PATH}")

def log_anomaly_event(model_name, mean_score, max_score, threshold=15.0):
    """ฟังก์ชันบันทึกผลการตรวจจับความผิดปกติจาก Edge Impulse โมเดล"""
    status = "DEFECT" if max_score > threshold else "NORMAL"
    alert = 1 if status == "DEFECT" else 0
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO anomaly_logs (model_name, anomaly_mean_score, anomaly_max_score, status, alert_triggered)
        VALUES (?, ?, ?, ?, ?)
    ''', (model_name, mean_score, max_score, status, alert))
    conn.commit()
    conn.close()
    print(f"[SQL Log] บันทึกเหตุการณ์ Anomaly: {status} (Max Score: {max_score:.2f}, Alert: {alert})")

def log_fomo_event(label, conf, x, y, w=16, h=16):
    """ฟังก์ชันบันทึกพิกัดวัตถุที่ตรวจพบโดยโมเดล FOMO"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO object_detection_logs (label, confidence, pos_x, pos_y, width, height)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (label, conf, x, y, w, h))
    conn.commit()
    conn.close()
    print(f"[SQL Log] บันทึกวัตถุ FOMO: '{label}' ที่พิกัด ({x}, {y}) ความมั่นใจ {conf*100:.1f}%")

def query_daily_summary():
    """ดึงรายงานสรุปสถิติประจำวัน"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT status, COUNT(*) 
        FROM anomaly_logs 
        GROUP BY status
    ''')
    rows = cursor.fetchall()
    
    print("\n--- สรุปสถิติผลการตรวจจับชิ้นงาน (Daily Inspection Report) ---")
    for status, count in rows:
        print(f" สถานะ {status}: {count} ครั้ง")
    conn.close()

if __name__ == "__main__":
    print("==================================================")
    print(" ทดสอบการทำงานของ Database-SQL Brick บน Arduino UNO Q")
    print("==================================================")
    init_database()
    
    # จำลองการส่งข้อมูลจากโมเดล AI บันทึกลงฐานข้อมูล
    print("\n[การจำลอง] 1. บันทึกผลชิ้นงานปกติ:")
    log_anomaly_event("vad_model.eim", mean_score=1.2, max_score=3.4)
    
    print("\n[การจำลอง] 2. บันทึกผลชิ้นงานพบรอยแตกร้าว (Defect):")
    log_anomaly_event("vad_model.eim", mean_score=18.5, max_score=42.1)
    
    print("\n[การจำลอง] 3. บันทึกการตรวจพบวัตถุด้วย FOMO:")
    log_fomo_event("brick_red", conf=0.92, x=48, y=52)

    # ดึงสถิติ
    query_daily_summary()
    print("==================================================")

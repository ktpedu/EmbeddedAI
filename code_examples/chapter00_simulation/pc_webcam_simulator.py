#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
เครื่องมือจำลองการประมวลผล Edge AI บนเครื่องคอมพิวเตอร์ (PC Webcam Simulator)
รายวิชา: ปัญญาประดิษฐ์บนระบบสมองกลฝังตัว (Embedded Artificial Intelligence)
--------------------------------------------------------------------------------
วัตถุประสงค์:
1. สำหรับผู้เรียนที่ไม่มีบอร์ดฮาร์ดแวร์ Arduino UNO Q เพื่อให้สามารถทดลองรันไปป์ไลน์
   การอนุมาน (Inference Pipeline) ร่วมกับกล้องเว็บแคมบนเครื่องคอมพิวเตอร์/โน้ตบุ๊กได้จริง
2. จำลองระบบ Visual Anomaly Detection, Image Classification และ Object Detection
3. จำลองระบบจัดเก็บบันทึกประวัติผลการตรวจจับลงฐานข้อมูล SQLite เสมือนบนตัวบอร์ด
================================================================================
"""

import sys
import os
import time
import sqlite3
import math

try:
    import cv2
    import numpy as np
except ImportError:
    print("[คำแนะนำ] กรุณาติดตั้ง OpenCV และ NumPy เพื่อใช้งานโปรแกรมจำลอง:")
    print("         pip install opencv-python numpy")
    sys.exit(1)

# กำหนดค่าตัวแปรระบบ
DB_PATH = os.path.join(os.path.dirname(__file__), "pc_edgeai_records.db")
WINDOW_NAME = "KT-Edu Edge AI Simulator (PC Webcam & Local Inference)"
CONFIDENCE_THRESHOLD = 0.75
ANOMALY_THRESHOLD = 0.60

def init_database():
    """สร้างฐานข้อมูล SQLite เสมือนจริงบนเครื่อง PC"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inference_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            model_type TEXT,
            label TEXT,
            confidence REAL,
            anomaly_score REAL,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()
    print(f"[*] เตรียมระบบฐานข้อมูลเสร็จสิ้น: {DB_PATH}")

def log_event(model_type, label, confidence, anomaly_score, status):
    """บันทึกประวัติการอนุมานลงในฐานข้อมูล"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO inference_logs (model_type, label, confidence, anomaly_score, status)
            VALUES (?, ?, ?, ?, ?)
        """, (model_type, label, confidence, anomaly_score, status))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[!] ไม่สามารถบันทึกลงฐานข้อมูล: {e}")

def main():
    init_database()
    print("[*] กำลังเปิดกล้องเว็บแคม (Device ID: 0)...")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("[!] ไม่พบกล้องเว็บแคม หรือกล้องถูกใช้งานโดยโปรแกรมอื่น")
        print("    กำลังเปิดโหมดสังเคราะห์ภาพทดสอบ (Synthetic Test Mode)...")
        use_synthetic = True
    else:
        use_synthetic = False
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    print("=======================================================")
    print(" เริ่มต้นระบบจำลอง Edge AI บนเครื่อง PC")
    print(" - กดปุ่ม [Space] : บันทึกภาพ Snapshot และ Log ลงฐานข้อมูล")
    print(" - กดปุ่ม [m]     : สลับโหมดจำลอง (Anomaly / Classification / Object Detection)")
    print(" - กดปุ่ม [q]     : ออกจากโปรแกรม")
    print("=======================================================")

    modes = ["Visual Anomaly Detection", "Image Classification", "Object Detection (FOMO)"]
    current_mode_idx = 0
    prev_time = time.time()
    fps = 0.0
    frame_count = 0

    while True:
        if not use_synthetic:
            ret, frame = cap.read()
            if not ret:
                print("[!] ไม่สามารถอ่านเฟรมภาพจากกล้องได้")
                break
            frame = cv2.flip(frame, 1) # Flip ภาพแบบกระจกเงา
        else:
            # สร้างเฟรมภาพทดสอบกรณีไม่มีกล้อง
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            frame[:] = (25, 30, 45)
            cv2.putText(frame, "Synthetic Camera Mode (No Physical Cam)", (80, 240),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 242, 255), 2)

        frame_count += 1
        curr_time = time.time()
        time_diff = curr_time - prev_time
        if time_diff >= 1.0:
            fps = frame_count / time_diff
            frame_count = 0
            prev_time = curr_time

        mode_name = modes[current_mode_idx]
        h, w, _ = frame.shape

        # -------------------------------------------------------------
        # จำลองการอนุมานของ Edge AI ตามโหมดที่เลือก
        # -------------------------------------------------------------
        sim_anomaly = 0.15 + 0.55 * (0.5 + 0.5 * math.sin(curr_time * 1.5))
        is_defect = sim_anomaly > ANOMALY_THRESHOLD

        # วาดแถบหัวข้อระบบ (Overlay Header)
        cv2.rectangle(frame, (0, 0), (w, 55), (15, 25, 45), -1)
        cv2.putText(frame, "KT-Edu Edge AI Simulator", (15, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 242, 255), 2)
        cv2.putText(frame, f"FPS: {fps:.1f} | Hardware: PC / Laptop Fallback", (15, 45),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 200, 200), 1)
        cv2.putText(frame, f"Mode: {mode_name}", (w - 300, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        if mode_name == "Visual Anomaly Detection":
            # แสดง Anomaly Score Bar
            bar_color = (0, 0, 255) if is_defect else (0, 255, 0)
            status_text = "DEFECT DETECTED!" if is_defect else "NORMAL (PASS)"
            cv2.rectangle(frame, (20, h - 60), (320, h - 25), (30, 30, 30), -1)
            bar_width = int(sim_anomaly * 290)
            cv2.rectangle(frame, (25, h - 55), (25 + bar_width, h - 30), bar_color, -1)
            cv2.putText(frame, f"Anomaly: {sim_anomaly:.3f} | {status_text}", (20, h - 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, bar_color, 2)

        elif mode_name == "Image Classification":
            labels = ["Circuit_Board_OK", "Component_Missing", "Background"]
            conf = 0.92
            cv2.rectangle(frame, (20, h - 70), (340, h - 20), (15, 25, 45), -1)
            cv2.putText(frame, f"Class: {labels[0]}", (30, h - 45),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv2.putText(frame, f"Confidence: {conf*100:.1f}%", (30, h - 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        elif mode_name == "Object Detection (FOMO)":
            # วาดกรอบ Bounding Box จำลอง
            cx, cy = int(w/2), int(h/2)
            cv2.circle(frame, (cx, cy), 12, (0, 242, 255), -1)
            cv2.rectangle(frame, (cx - 60, cy - 60), (cx + 60, cy + 60), (0, 242, 255), 2)
            cv2.putText(frame, "Part_A [0.89]", (cx - 60, cy - 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 242, 255), 2)

        # คำแนะนำปุ่มลัด
        cv2.putText(frame, "[Space] Log Data | [m] Change Mode | [q] Quit", (w - 380, h - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (180, 180, 180), 1)

        cv2.imshow(WINDOW_NAME, frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break
        elif key == ord('m'):
            current_mode_idx = (current_mode_idx + 1) % len(modes)
            print(f"[*] เปลี่ยนโหมดเป็น: {modes[current_mode_idx]}")
        elif key == 32: # Space bar
            status_desc = "DEFECT" if is_defect else "NORMAL"
            log_event(mode_name, "Simulated_Object", 0.88, sim_anomaly, status_desc)
            print(f"[+] บันทึก Log สำเร็จ: Mode={mode_name}, Anomaly={sim_anomaly:.3f}, Status={status_desc}")

    if not use_synthetic:
        cap.release()
    cv2.destroyAllWindows()
    print("[*] ปิดระบบจำลองเรียบร้อยแล้ว")

if __name__ == "__main__":
    main()

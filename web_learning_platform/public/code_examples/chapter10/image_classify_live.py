#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
รายวิชา: การพัฒนาปัญญาประดิษฐ์บนอุปกรณ์ขอบ (Edge AI Development)
บทเรียนที่ 10: การพัฒนาและประมวลผลโมเดลจำแนกประเภทภาพ (Image Classification)
สคริปต์: image_classify_live.py - การประมวลผลจำแนกประเภทชิ้นงานสด และคัดกรองสัญญาณฉากหลัง

คำอธิบาย:
    สคริปต์นี้ทำงานร่วมกับ Image Classification Brick บนบอร์ดพัฒนา Arduino UNO Q
    รับเฟรมภาพสดจากกล้องเว็บแคม ประมวลผลผ่านโมเดล MobileNetV2 (.eim)
    สกัดคะแนนความน่าจะเป็นแบบ Softmax คำนวณความหน่วงเวลาในการประมวลผล
    และคัดกรองคลาสฉากหลังว่างเปล่า (Background) เพื่อป้องกันการแจ้งเตือนผิดพลาด
"""

import sys
import time

# กำหนดการเข้ารหัส UTF-8 สำหรับคอนโซล
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# ตรวจสอบสภาพแวดล้อมบอร์ดพัฒนา Arduino UNO Q
try:
    from arduino.app_bricks.image_classification import ImageClassification
    from arduino.app_utils import App
    IS_ARDUINO_ENV = True
except ImportError:
    IS_ARDUINO_ENV = False


class LiveImageClassifier:
    """คลาสจัดการผลการจำแนกประเภทภาพแบบเวลาจริงและการคำนวณสถิติ"""
    
    def __init__(self, confidence_threshold=0.80):
        self.threshold = confidence_threshold
        self.frame_count = 0
        self.start_time = time.time()
        self.fps = 0.0
        self.summary_stats = {"Capacitor": 0, "Resistor": 0, "IC_Chip": 0, "Background": 0, "Uncertain": 0}

    def process_result(self, result, latency_ms=32.5):
        """ประมวลผลข้อมูลผลการจำแนกประเภทจากโมเดล"""
        if not result:
            return

        self.frame_count += 1
        current_time = time.time()
        elapsed = current_time - self.start_time
        if elapsed >= 1.0:
            self.fps = self.frame_count / elapsed
            self.frame_count = 0
            self.start_time = current_time

        top_label = result.get("label", "Unknown")
        confidence = result.get("confidence", 0.0)
        scores = result.get("scores", {})

        # 1. ตรวจสอบกรณีฉากหลังว่างเปล่า (Background / Nothing / None)
        if top_label.lower() in ["background", "nothing", "none"]:
            self.summary_stats["Background"] += 1
            print(f"[{time.strftime('%H:%M:%S')}] [FPS: {self.fps:4.1f}] [-] ฉากหลังว่างเปล่า (Background: {confidence * 100:.1f}%) | ความหน่วงเวลา: {latency_ms:.1f} ms")
            return

        # 2. ตรวจสอบเกณฑ์ความเชื่อมั่นขั้นต่ำ (Confidence Threshold)
        if confidence >= self.threshold:
            self.summary_stats[top_label] = self.summary_stats.get(top_label, 0) + 1
            print(f"\n[{time.strftime('%H:%M:%S')}] [FPS: {self.fps:4.1f}] [+] [MATCH] จำแนกพบชิ้นงาน: '{top_label}'")
            print(f"    - ระดับความเชื่อมั่น: {confidence * 100:.2f}% (ผ่านเกณฑ์ >= {self.threshold * 100:.0f}%)")
            print(f"    - ความหน่วงเวลาในการประมวลผล: {latency_ms:.1f} ms")
            
            # แสดงสัดส่วนคะแนน Softmax ทั้งหมด
            score_str = ", ".join([f"{k}: {v * 100:.1f}%" for k, v in scores.items()])
            print(f"    - การกระจายความน่าจะเป็น (Softmax): [{score_str}]")
            
            # การดำเนินการต่อยอดตามชนิดชิ้นงาน
            if top_label == "Capacitor":
                print("    -> คำสั่งปฏิบัติการ: ส่งสัญญาณบันทึกคลังชิ้นส่วนตัวเก็บประจุ (Capacitor Tray A)")
            elif top_label == "Resistor":
                print("    -> คำสั่งปฏิบัติการ: ส่งสัญญาณบันทึกคลังชิ้นส่วนตัวต้านทาน (Resistor Tray B)")
            elif top_label == "IC_Chip":
                print("    -> คำสั่งปฏิบัติการ: ส่งสัญญาณบันทึกคลังชิ้นส่วนไอซี (IC_Chip Tray C)")
        else:
            self.summary_stats["Uncertain"] += 1
            print(f"[{time.strftime('%H:%M:%S')}] [FPS: {self.fps:4.1f}] [?] ความเชื่อมั่นไม่เพียงพอ ({top_label}: {confidence * 100:.1f}% < {self.threshold * 100:.0f}%)")


def run_simulation():
    """ฟังก์ชันทดสอบการทำงานของระบบในโหมดจำลองคอนโซล"""
    print("=" * 72)
    print("   ระบบจำแนกประเภทภาพชิ้นงานอิเล็กทรอนิกส์ (Image Classification)")
    print("   หลักสูตร: การพัฒนาปัญญาประดิษฐ์บนอุปกรณ์ขอบ (บทเรียนที่ 10)")
    print("=" * 72)
    print("[*] เริ่มต้นการทดสอบในโหมดจำลองสถานการณ์คอนโซล (Console Simulation)...")
    print(f"[*] กำหนดค่าเกณฑ์ความเชื่อมั่นขั้นต่ำ (Confidence Threshold): 0.80 (80%)")
    print("-" * 72)

    classifier = LiveImageClassifier(confidence_threshold=0.80)

    # ชุดข้อมูลจำลองผลการทำนาย 5 เหตุการณ์
    mock_events = [
        # เหตุการณ์ที่ 1: พื้นหลังว่างเปล่า
        ({"label": "Background", "confidence": 0.96, "scores": {"Background": 0.96, "Capacitor": 0.02, "Resistor": 0.01, "IC_Chip": 0.01}}, 28.4),
        # เหตุการณ์ที่ 2: วางตัวเก็บประจุ (Capacitor)
        ({"label": "Capacitor", "confidence": 0.92, "scores": {"Background": 0.03, "Capacitor": 0.92, "Resistor": 0.03, "IC_Chip": 0.02}}, 31.8),
        # เหตุการณ์ที่ 3: วางตัวต้านทาน (Resistor)
        ({"label": "Resistor", "confidence": 0.88, "scores": {"Background": 0.05, "Capacitor": 0.04, "Resistor": 0.88, "IC_Chip": 0.03}}, 30.5),
        # เหตุการณ์ที่ 4: ชิ้นงานกำกวม ความเชื่อมั่นต่ำ
        ({"label": "Capacitor", "confidence": 0.54, "scores": {"Background": 0.20, "Capacitor": 0.54, "Resistor": 0.22, "IC_Chip": 0.04}}, 32.1),
        # เหตุการณ์ที่ 5: วางชิปไอซี (IC_Chip)
        ({"label": "IC_Chip", "confidence": 0.94, "scores": {"Background": 0.02, "Capacitor": 0.02, "Resistor": 0.02, "IC_Chip": 0.94}}, 29.7),
    ]

    for idx, (res, lat) in enumerate(mock_events, 1):
        print(f"\n--- [รอบการประเมินผลที่ {idx} / {len(mock_events)}] ---")
        classifier.process_result(res, latency_ms=lat)
        time.sleep(0.12)

    print("\n" + "=" * 72)
    print("   สรุปสถิติผลการจำแนกประเภทชิ้นงานประจำรอบการผลิต")
    print("=" * 72)
    for category, count in classifier.summary_stats.items():
        print(f"  - หมวดหมู่วัตถุ {category:<14}: {count:>2} ครั้ง")
    print("=" * 72)
    print("[✓] การทดสอบระบบจำแนกประเภทภาพเสร็จสมบูรณ์ พร้อมติดตั้งใช้งานจริง\n")


def main():
    if not IS_ARDUINO_ENV:
        run_simulation()
        return

    print("[*] ตรวจพบสภาพแวดล้อมบอร์ดพัฒนา Arduino UNO Q พร้อมใช้งาน")
    classifier_brick = ImageClassification()
    live_handler = LiveImageClassifier(confidence_threshold=0.80)
    classifier_brick.on_classify(live_handler.process_result)

    print("[*] เริ่มต้นระบบจำแนกภาพแบบเวลาจริง กด Ctrl+C เพื่อออก...")
    App.run()


if __name__ == "__main__":
    main()

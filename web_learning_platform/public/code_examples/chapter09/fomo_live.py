#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
รายวิชา: การพัฒนาปัญญาประดิษฐ์บนอุปกรณ์ขอบ (Edge AI Development)
บทเรียนที่ 9: การนำโมเดล FOMO ไปใช้งานและการควบคุมอุปกรณ์ขับเคลื่อน (Actuator)
สคริปต์: fomo_live.py - การประมวลผลโมเดล FOMO ตรวจจับวัตถุสด คำนวณพิกัดจุดกึ่งกลาง และควบคุมอุปกรณ์ขับเคลื่อน

คำอธิบาย:
    สคริปต์นี้ทำงานร่วมกับ Video Object Detection Brick และระบบควบคุมอุปกรณ์ขับเคลื่อน (Actuator)
    บนบอร์ดพัฒนา Arduino UNO Q โดยดึงเฟรมภาพจากกล้องเว็บแคม ประมวลผลผ่านโมเดล FOMO (.eim)
    สกัดพิกัดจุดกึ่งกลาง (Centroid X, Y) ของวัตถุ และส่งสัญญาณควบคุมเซอร์โวมอเตอร์คัดแยกชิ้นงาน
"""

import sys
import time
import math

# กำหนดการเข้ารหัสมาตรฐาน UTF-8 สำหรับคอนโซล
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# ตรวจสอบการนำเข้ามอดูลของบอร์ดพัฒนา Arduino UNO Q
try:
    from arduino.app_bricks.video_object_detection import VideoObjectDetection
    from arduino.app_utils import App
    IS_ARDUINO_ENV = True
except ImportError:
    IS_ARDUINO_ENV = False


class ActuatorController:
    """คลาสควบคุมอุปกรณ์ขับเคลื่อน (Actuator / Servo Motor / Relay) สำหรับคัดแยกชิ้นงาน"""
    
    def __init__(self, servo_pin=9, relay_pin=7):
        self.servo_pin = servo_pin
        self.relay_pin = relay_pin
        self.current_angle = 90  # องศาตั้งต้น (ตรงกลาง - พักการทำงาน)
        self.is_busy = False
        
    def move_servo(self, target_angle, action_name=""):
        """ส่งสัญญาณควบคุมมุมองศาของเซอร์โวมอเตอร์เพื่อผลัก/คัดแยกชิ้นงาน"""
        self.is_busy = True
        self.current_angle = target_angle
        print(f"    [Actuator] สั่งการพิน {self.servo_pin}: หมุนก้านปัดไปยังมุม {target_angle}° ({action_name})")
        time.sleep(0.05)  # จำลองช่วงเวลาการเคลื่อนที่ของเซอร์โวมอเตอร์
        self.is_busy = False

    def trigger_relay(self, state=True, duration=0.1):
        """ส่งสัญญาณเปิด/ปิดรีเลย์เพื่อควบคุมไฟสัญญาณแจ้งเตือนหรือสายพานลำเลียง"""
        status_text = "เปิดทำงาน (ON)" if state else "ปิดทำงาน (OFF)"
        print(f"    [Relay] สั่งการพิน {self.relay_pin}: {status_text}")


class FomoLiveInspector:
    """คลาสประมวลผลผลลัพธ์จากโมเดล FOMO และประสานงานกับอุปกรณ์ขับเคลื่อน"""
    
    def __init__(self, confidence_threshold=0.65):
        self.threshold = confidence_threshold
        self.actuator = ActuatorController(servo_pin=9, relay_pin=7)
        self.frame_count = 0
        self.start_time = time.time()
        self.fps = 0.0
        self.total_sorted = {"Bolt": 0, "Nut": 0, "Bearing": 0, "Unknown": 0}

    def process_detections(self, detections):
        """วิเคราะห์รายการวัตถุที่ตรวจพบ สกัดพิกัดจุดกึ่งกลาง และสั่งการอุปกรณ์ขับเคลื่อน"""
        self.frame_count += 1
        current_time = time.time()
        elapsed = current_time - self.start_time
        
        if elapsed >= 1.0:
            self.fps = self.frame_count / elapsed
            self.frame_count = 0
            self.start_time = current_time

        if not detections:
            print(f"[{time.strftime('%H:%M:%S')}] [FPS: {self.fps:4.1f}] กำลังเฝ้าระวังพื้นที่สายพาน... ไม่พบวัตถุ")
            return

        valid_detections = [item for item in detections if getattr(item, 'confidence', 0.0) >= self.threshold]
        
        if not valid_detections:
            print(f"[{time.strftime('%H:%M:%S')}] [FPS: {self.fps:4.1f}] ตรวจพบสัญญาณรบกวนแต่ค่าความเชื่อมั่นต่ำกว่าเกณฑ์ {self.threshold:.2f}")
            return

        print(f"\n[{time.strftime('%H:%M:%S')}] [FPS: {self.fps:4.1f}] ตรวจพบวัตถุผ่านเกณฑ์จำนวน {len(valid_detections)} ชิ้นงาน:")
        
        for idx, item in enumerate(valid_detections, 1):
            label = getattr(item, 'label', 'Unknown')
            confidence = getattr(item, 'confidence', 0.0)
            x = getattr(item, 'x', 0)
            y = getattr(item, 'y', 0)
            width = getattr(item, 'width', 0)
            height = getattr(item, 'height', 0)
            
            # คำนวณพิกัดจุดกึ่งกลาง (Centroid)
            cx = x + (width // 2) if width > 0 else x
            cy = y + (height // 2) if height > 0 else y
            
            print(f"  ชิ้นที่ {idx}: วัตถุ [{label}] ความเชื่อมั่น: {confidence * 100:.1f}%")
            print(f"    - พิกัดจุดกึ่งกลาง (Centroid): ({cx}, {cy}) | ขอบเขตกรอบ: {width}x{height} พิกเซล")
            
            # ตรรกะการควบคุมอุปกรณ์ขับเคลื่อนตามชนิดของวัตถุและพิกัดตำแหน่ง
            if label.lower() == "bolt":
                self.actuator.move_servo(45, "คัดแยกสลักเกลียว -> ลงกล่องซ้าย A")
                self.total_sorted["Bolt"] += 1
            elif label.lower() == "nut":
                self.actuator.move_servo(135, "คัดแยกแป้นเกลียว -> ลงกล่องขวา B")
                self.total_sorted["Nut"] += 1
            elif label.lower() == "bearing":
                self.actuator.move_servo(90, "ชิ้นงานตลับลูกปืน -> ปล่อยผ่านสายพานตรง C")
                self.total_sorted["Bearing"] += 1
            else:
                self.actuator.move_servo(0, "วัตถุแปลกปลอม -> ผลักลงกล่องตรวจสอบ D")
                self.actuator.trigger_relay(True)
                self.total_sorted["Unknown"] += 1


class MockDetectionItem:
    """คลาสจำลองอ็อบเจกต์ผลลัพธ์การตรวจจับสำหรับทดสอบบนคอนโซล"""
    def __init__(self, label, confidence, x, y, width=28, height=28):
        self.label = label
        self.confidence = confidence
        self.x = x
        self.y = y
        self.width = width
        self.height = height


def run_simulation():
    """ฟังก์ชันทดสอบการทำงานของระบบในโหมดจำลองคอนโซล"""
    print("=" * 72)
    print("   ระบบตรวจจับตำแหน่งวัตถุ FOMO และควบคุมอุปกรณ์ขับเคลื่อน (Actuator)")
    print("   หลักสูตร: การพัฒนาปัญญาประดิษฐ์บนอุปกรณ์ขอบ (บทเรียนที่ 9)")
    print("=" * 72)
    print("[*] กำลังเริ่มต้นการทดสอบในโหมดจำลองสถานการณ์คอนโซล (Console Simulation)...")
    print("[*] กำหนดค่าเกณฑ์ความเชื่อมั่น (Confidence Threshold): 0.65")
    print("-" * 72)

    inspector = FomoLiveInspector(confidence_threshold=0.65)

    test_frames = [
        # เฟรมที่ 1: ตรวจพบ Bolt (สลักเกลียว)
        [MockDetectionItem("Bolt", 0.94, 85, 110, 32, 32)],
        # เฟรมที่ 2: ตรวจพบ Nut (แป้นเกลียว)
        [MockDetectionItem("Nut", 0.89, 142, 98, 24, 24)],
        # เฟรมที่ 3: ตรวจพบหลายชิ้นพร้อมกัน (Bolt + Bearing)
        [MockDetectionItem("Bolt", 0.91, 60, 105, 30, 30),
         MockDetectionItem("Bearing", 0.87, 180, 115, 36, 36)],
        # เฟรมที่ 4: สัญญาณรบกวนความเชื่อมั่นต่ำ
        [MockDetectionItem("Nut", 0.45, 90, 80, 20, 20)],
        # เฟรมที่ 5: ชิ้นส่วนแปลกปลอม (Unknown Defect)
        [MockDetectionItem("Unknown", 0.82, 120, 130, 40, 40)]
    ]

    for frame_idx, frame_data in enumerate(test_frames, 1):
        print(f"\n--- [รอบการตรวจสอบที่ {frame_idx} / {len(test_frames)}] ---")
        inspector.process_detections(frame_data)
        time.sleep(0.15)

    print("\n" + "=" * 72)
    print("   สรุปผลการคัดแยกวัตถุโดยระบบอุปกรณ์ขับเคลื่อนอัตโนมัติ")
    print("=" * 72)
    for category, count in inspector.total_sorted.items():
        print(f"  - กลุ่มชิ้นงาน {category:<12}: {count:>2} ชิ้น")
    total_items = sum(inspector.total_sorted.values())
    print(f"  รวมทั้งสิ้น: {total_items} ชิ้นงาน")
    print("=" * 72)
    print("[✓] การทดสอบระบบสมบูรณ์ พร้อมนำไปเชื่อมต่อบนบอร์ดพัฒนา Arduino UNO Q\n")


def main():
    if not IS_ARDUINO_ENV:
        run_simulation()
        return

    # กรณีทำงานบนบอร์ดพัฒนา Arduino UNO Q
    print("[*] ตรวจพบสภาพแวดล้อม Arduino UNO Q พร้อมใช้งาน")
    detector = VideoObjectDetection()
    inspector = FomoLiveInspector(confidence_threshold=0.65)
    detector.on_detect(inspector.process_detections)
    
    print("[*] เริ่มต้นการตรวจจับวัตถุสดและควบคุมเซอร์โวมอเตอร์ กด Ctrl+C เพื่อหยุดการทำงาน...")
    App.run()


if __name__ == "__main__":
    main()

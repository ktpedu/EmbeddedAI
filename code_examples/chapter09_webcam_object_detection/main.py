#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
รายวิชาเพิ่มเติม: ปัญญาประดิษฐ์บนระบบสมองกลฝังตัว (Embedded Artificial Intelligence)
บทเรียนที่ 9: การเทรนโมเดล AI ให้ใช้กับงาน Object Detection (Brick) ผ่านกล้องเว็ปแคม
สคริปต์: การประมวลผลวิดีโอสด ตรวจจับวัตถุ คำนวณ FPS และส่งออกผลลัพธ์สู่ Web UI (Port 7000)

คำอธิบาย:
    สคริปต์นี้ทำงานร่วมกับโมดูล video_object_detection และ web_ui ของระบบ Arduino App Lab
    เพื่อดึงเฟรมภาพจากกล้องเว็บแคมยูเอสบีแบบเวลาจริง ประมวลผลผ่านโมเดล FOMO (.eim)
    คำนวณอัตราเร็วเฟรมภาพ (FPS) แสดงพิกัดและค่าความเชื่อมั่น และสตรีมมิงขึ้นสู่หน้าเว็บ
"""

import time
import sys

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

try:
    from arduino.app_bricks.video_object_detection import VideoObjectDetection
    from arduino.app_utils import App
    IS_ARDUINO_ENV = True
except ImportError:
    IS_ARDUINO_ENV = False

class ObjectDetectionMonitor:
    def __init__(self, confidence_threshold=0.65):
        self.threshold = confidence_threshold
        self.frame_count = 0
        self.start_time = time.time()
        self.fps = 0.0

    def on_frame_detected(self, detections):
        """Callback ฟังก์ชันประมวลผลข้อมูลวัตถุที่ตรวจพบในแต่ละเฟรม"""
        self.frame_count += 1
        current_time = time.time()
        elapsed = current_time - self.start_time
        
        # คำนวณ FPS ทุก ๆ 1 วินาที
        if elapsed >= 1.0:
            self.fps = self.frame_count / elapsed
            self.frame_count = 0
            self.start_time = current_time

        if detections:
            print(f"\n[FPS: {self.fps:4.1f}] ตรวจพบวัตถุจำนวน {len(detections)} รายการ:")
            for item in detections:
                label = getattr(item, 'label', 'Object')
                confidence = getattr(item, 'confidence', 0.0)
                x = getattr(item, 'x', 0)
                y = getattr(item, 'y', 0)
                width = getattr(item, 'width', 0)
                height = getattr(item, 'height', 0)
                
                if confidence >= self.threshold:
                    print(f"  -> [{label:<12}] ความเชื่อมั่น: {confidence*100:5.1f}% | จุดศูนย์กลาง: ({x:3d}, {y:3d}) | ขนาด: {width}x{height} px")
                    
                    # ตรรกะประยุกต์ใช้งาน: แยกแยะวัตถุ
                    if label.lower() == "tap":
                        pass  # สามารถสั่งงานพินหรือส่งข้อมูลต่อไปยัง MCU ได้ที่นี่
        else:
            # ไม่พบวัตถุในเฟรมนี้
            sys.stdout.write(f"\r[FPS: {self.fps:4.1f}] กำลังเฝ้าระวัง... ไม่พบวัตถุเป้าหมายในภาพ")
            sys.stdout.flush()

def main():
    print("=" * 65)
    print(" ระบบตรวจจับวัตถุแบบเวลาจริงผ่านกล้องเว็บแคม (Webcam Object Detection)")
    print(" สตรีมมิงการแสดงผลสู่ Web UI Dashboard ที่: http://<IP_ADDRESS>:7000")
    print("=" * 65)
    
    if not IS_ARDUINO_ENV:
        print("[!] ไม่พบสภาพแวดล้อม Arduino App Lab (กำลังทดสอบในโหมดจำลองคอนโซล)")
        print("[*] ตัวอย่างผลการตรวจจับจำลอง:")
        monitor = ObjectDetectionMonitor(confidence_threshold=0.65)
        class MockItem:
            def __init__(self, label, conf, x, y, w, h):
                self.label = label
                self.confidence = conf
                self.x, self.y = x, y
                self.width, self.height = w, h
                
        mock_data = [MockItem("Tap", 0.92, 160, 120, 48, 52), MockItem("DHT11", 0.88, 80, 95, 36, 40)]
        monitor.on_frame_detected(mock_data)
        return

    detector = VideoObjectDetection()
    monitor = ObjectDetectionMonitor(confidence_threshold=0.65)
    detector.on_detect(monitor.on_frame_detected)
    
    print("[*] เริ่มต้นการประมวลผลวิดีโอสด กด Ctrl+C เพื่อออก...")
    App.run()

if __name__ == "__main__":
    main()

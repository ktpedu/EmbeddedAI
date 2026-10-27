#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
หลักสูตร: ปัญญาประดิษฐ์บนระบบสมองกลฝังตัว (Embedded Artificial Intelligence)
บทที่ 2: สถาปัตยกรรมซอฟต์แวร์แบบมอดูล (Modular Brick) และการควบคุมฮาร์ดแวร์พื้นฐาน
ไฟล์: brick_runner.py

วัตถุประสงค์:
1. สาธิตการสร้างคลาส Custom Brick ตามมาตรฐาน Arduino App Lab
2. ควบคุมการแสดงผลบนแผงไฟ LED Matrix ในตัวบอร์ด Arduino UNO Q
3. ตรวจจับสัญญาณอินพุตจากสวิตช์ปุ่มกด (User Button) พร้อมอัลกอริทึม Software Debouncing
4. สื่อสารแลกเปลี่ยนคำสั่งระหว่าง MPU (Qualcomm Linux) และ MCU (ARM Cortex-M4) ผ่านระบบบัส IPC
"""

import time
import sys
import logging

# บังคับการแสดงผลภาษาไทยบนคอนโซลให้ถูกต้อง
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# กำหนดค่าระบบบันทึกข้อความ (Logging)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)

# นำเข้าโมดูลฮาร์ดแวร์และโครงสร้างแอปพลิเคชันจากไลบรารีทางการของ Arduino App Lab
try:
    from arduino.app_utils import App
    from arduino.peripherals import Matrix, Pin
    IS_HARDWARE_AVAILABLE = True
except ImportError:
    IS_HARDWARE_AVAILABLE = False
    logging.warning("ไม่พบไลบรารีฮาร์ดแวร์ กำลังทำงานในโหมดจำลอง (Simulator Mode)")

class HardwareControlBrick:
    """
    มอดูลซอฟต์แวร์สำหรับควบคุมการแสดงผลบนแผงไฟ LED Matrix
    และจัดการเหตุการณ์การกดสวิตช์ปุ่มกด (Active-Low)
    """
    def __init__(self):
        self.state_index = 0
        self.icons = ["READY", "AI_ACTIVE", "WARNING"]
        
        if IS_HARDWARE_AVAILABLE:
            self.matrix = Matrix()
            # กำหนดพินปุ่มกดเป็น Input พร้อมเปิดตัวต้านทาน Pull-up ภายใน
            self.button = Pin("USER_BTN", Pin.IN_PULLUP)
        else:
            self.matrix = None
            self.button = None
        
        logging.info("มอดูล HardwareControlBrick เริ่มต้นการทำงานสำเร็จ")

    def on_start(self):
        """สั่งทำงานเมื่อเริ่มต้นโปรแกรม"""
        logging.info("กำลังเตรียมความพร้อมอุปกรณ์แสดงผล...")
        if self.matrix:
            self.matrix.show_icon("CHECK")  # แสดงสัญลักษณ์เครื่องหมายถูก
            time.sleep(1.0)
            self.matrix.clear()
        logging.info("บอร์ดพร้อมตรวจรับเหตุการณ์และรันโมเดล")

    def update(self):
        """วนลูปตรวจสอบสัญญาณปุ่มกดและอัปเดตการแสดงผล"""
        if self.button and not self.button.read():  # Active-Low: 0 คือกด
            self.state_index = (self.state_index + 1) % len(self.icons)
            current_mode = self.icons[self.state_index]
            logging.info(f"ผู้ใช้กดปุ่ม: สลับสู่โหมดการทำงาน -> {current_mode}")
            
            if self.matrix:
                self.matrix.show_icon(current_mode)
            
            # ป้องกันปัญหาการกระดอนของหน้าสัมผัสสวิตช์ (Software Debouncing)
            time.sleep(0.25)

    def on_stop(self):
        """คืนค่าและปิดการทำงานอย่างปลอดภัยเมื่อปิดโปรแกรม"""
        if self.matrix:
            self.matrix.clear()
        logging.info("ปิดการทำงานของฮาร์ดแวร์อย่างปลอดภัย")

if __name__ == "__main__":
    # สร้างอินสแตนซ์ศูนย์กลางของแอปพลิเคชัน
    app = App()
    
    # ลงทะเบียนมอดูลฮาร์ดแวร์เข้าสู่ระบบ
    hw_brick = HardwareControlBrick()
    app.register_brick(hw_brick)
    
    # เริ่มต้นวงรอบการประมวลผลหลัก (Main Application Loop)
    logging.info("เริ่มต้นการรันระบบ Modular Brick Runner...")
    try:
        app.run()
    except KeyboardInterrupt:
        logging.info("ตรวจพบสัญญาณหยุดการทำงาน (SIGINT / Ctrl+C)")
        hw_brick.on_stop()

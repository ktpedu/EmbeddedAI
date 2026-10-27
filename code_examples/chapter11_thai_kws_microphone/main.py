#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
รายวิชาเพิ่มเติม: ปัญญาประดิษฐ์บนระบบสมองกลฝังตัว (Embedded Artificial Intelligence)
บทเรียนที่ 11: การเทรนโมเดล AI ให้ใช้กับงาน Keyword Spotting (Brick) ผ่านไมโครโฟน (คำสั่งไทย)
สคริปต์: การตรวจจับคำสั่งเสียงภาษาไทยผ่านไมโครโฟน และควบคุมอุปกรณ์เอาต์พุต (LED / Relay)

คำอธิบาย:
    สคริปต์นี้เรียกใช้งานโมดูล KeywordSpotting Brick เพื่อรับสัญญาณเสียงพูดภาษาไทยผ่านไมโครโฟน
    ทำการตรวจจับคำสั่งเป้าหมาย เช่น "open" (เปิด), "close" (ปิด), "red" (แดง), "green" (เขียว)
    พร้อมทั้งคัดกรองคำออกเสียงคล้ายในคลาส 'unknown' (เช่น แดน, แทง, เปิป) ออกจากระบบ
"""

import time
import sys

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

try:
    from arduino.app_bricks.keyword_spotting import KeywordSpotting
    from arduino.app_utils import App
    IS_ARDUINO_ENV = True
except ImportError:
    IS_ARDUINO_ENV = False

# จำลองสถานะพินฮาร์ดแวร์เอาต์พุต
hardware_state = {
    "lamp_relay": False,
    "led_red": False,
    "led_green": False
}

def execute_thai_command(command_label: str):
    """แปลคำสั่งเสียงภาษาไทยและสั่งการทำงานของอุปกรณ์"""
    cmd = command_label.lower().strip()
    print(f"\n[VOICE COMMAND] ได้รับคำสั่งเสียง: '{command_label}'")
    
    if cmd in ["open", "เปิด"]:
        hardware_state["lamp_relay"] = True
        print("  -> สั่งการ: [เปิดไฟส่องสว่าง] สัญญาณ Relay = ON (Active HIGH)")
    elif cmd in ["close", "ปิด"]:
        hardware_state["lamp_relay"] = False
        print("  -> สั่งการ: [ปิดไฟส่องสว่าง] สัญญาณ Relay = OFF (LOW)")
    elif cmd in ["red", "แดง"]:
        hardware_state["led_red"] = True
        hardware_state["led_green"] = False
        print("  -> สั่งการ: [เปิดไฟเตือนสีแดง] LED RED = ON | LED GREEN = OFF")
    elif cmd in ["green", "เขียว"]:
        hardware_state["led_green"] = True
        hardware_state["led_red"] = False
        print("  -> สั่งการ: [เปิดไฟสถานะสีเขียว] LED GREEN = ON | LED RED = OFF")
    elif cmd in ["unknown", "noise"]:
        print("  -> สถานะ: ตรวจพบเสียงอื่นหรือคำพ้องเสียงที่ไม่ใช่คำสั่งเป้าหมาย (เพิกเฉยคำสั่ง)")
    else:
        print(f"  -> คำสั่งไม่ตรงกับเงื่อนไขในระบบ: {cmd}")

def setup_thai_kws_system():
    print("=" * 65)
    print(" ระบบรู้จำคำสั่งเสียงภาษาไทยผ่านไมโครโฟน (Thai Keyword Spotting)")
    print(" รองรับคำสั่ง: 'เปิด', 'ปิด', 'แดง', 'เขียว' (พร้อมระบบกรองคลาส Unknown)")
    print("=" * 65)
    
    if not IS_ARDUINO_ENV:
        print("[!] กำลังรันในโหมดจำลอง (Simulated Mode นอกบอร์ด UNO Q)")
        print("[*] ทดสอบจำลองการส่งคำสั่งเสียง:")
        execute_thai_command("เปิด")
        execute_thai_command("แดง")
        execute_thai_command("unknown")  # คำที่ออกเสียงคล้าย เช่น แดน/แทง
        execute_thai_command("ปิด")
        return

    spotter = KeywordSpotting(confidence=0.85, debounce_sec=2.5)
    time.sleep(1.0)
    
    info = spotter.get_model_info()
    if info is not None:
        print(f"[-] คลาสที่โหลดจากโมเดล: {info.labels}")
        for label in info.labels:
            def make_callback(l):
                def callback():
                    execute_thai_command(l)
                return callback
            spotter.on_detect(label, make_callback(label))
            
    print("[*] ระบบพร้อมรับคำสั่งเสียงภาษาไทยผ่านไมโครโฟน กด Ctrl+C เพื่อออก...")
    App.run()

if __name__ == "__main__":
    setup_thai_kws_system()

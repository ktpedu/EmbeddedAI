#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
รายวิชา: การพัฒนาปัญญาประดิษฐ์บนอุปกรณ์ขอบ (Edge AI Development)
บทเรียนที่ 11: การรู้จำคำสั่งเสียงภาษาไทยผ่านไมโครโฟน (Thai Keyword Spotting)
สคริปต์: thai_kws_live.py - การตรวจจับคำสั่งเสียงภาษาไทย และควบคุมอุปกรณ์ฮาร์ดแวร์เอาต์พุต

คำอธิบาย:
    สคริปต์นี้ทำงานร่วมกับ Keyword Spotting Brick บนบอร์ดพัฒนา Arduino UNO Q
    เพื่อรับสัญญาณเสียงพูดภาษาไทยผ่านไมโครโฟนดิจิทัล ประมวลผลผ่านโมเดล MFCC-CNN (.eim)
    แยกแยะคำสั่งภาษาไทย: 'เปิด', 'ปิด', 'แดง', 'เขียว' พร้อมทั้งคัดกรองเสียงรบกวน
    และคำใกล้เคียงในคลาส 'unknown' เพื่อป้องกันการสั่งงานผิดพลาด
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
    from arduino.app_bricks.keyword_spotting import KeywordSpotting
    from arduino.app_utils import App
    IS_ARDUINO_ENV = True
except ImportError:
    IS_ARDUINO_ENV = False


class ThaiVoiceCommander:
    """คลาสจัดการการตรวจจับคำสั่งเสียงภาษาไทยและควบคุมฮาร์ดแวร์เอาต์พุต"""
    
    def __init__(self, confidence_threshold=0.85, debounce_sec=2.0):
        self.threshold = confidence_threshold
        self.debounce_sec = debounce_sec
        self.last_trigger_time = 0.0
        self.last_command = ""
        self.hardware_state = {
            "lamp_relay": False,
            "led_red": False,
            "led_green": False
        }
        self.stats = {"เปิด": 0, "ปิด": 0, "แดง": 0, "เขียว": 0, "unknown": 0, "noise": 0}

    def execute_command(self, label: str, confidence: float = 0.90):
        """วิเคราะห์และสั่งการทำงานตามคำสั่งเสียงภาษาไทยที่ตรวจพบ"""
        current_time = time.time()
        cmd = label.lower().strip()

        # 1. ตรวจสอบการหน่วงเวลาเพื่อป้องกันคำสั่งซ้ำซ้อน (Debouncing)
        if (current_time - self.last_trigger_time) < self.debounce_sec and cmd == self.last_command:
            print(f"[{time.strftime('%H:%M:%S')}] [!] คำสั่ง '{label}' ถูกปฏิเสธ (อยู่ในช่วง Debounce Lock {self.debounce_sec:.1f} วินาที)")
            return

        # 2. ตรวจสอบเกณฑ์ความเชื่อมั่นขั้นต่ำ
        if confidence < self.threshold:
            print(f"[{time.strftime('%H:%M:%S')}] [?] ตรวจพบเสียงคล้าย '{label}' แต่ความเชื่อมั่นต่ำ ({confidence*100:.1f}% < {self.threshold*100:.0f}%)")
            return

        self.last_trigger_time = current_time
        self.last_command = cmd

        print(f"\n[{time.strftime('%H:%M:%S')}] [VOICE DETECTED] รับคำสั่งเสียง: '{label}' (ความเชื่อมั่น: {confidence * 100:.2f}%)")

        if cmd in ["open", "เปิด"]:
            self.hardware_state["lamp_relay"] = True
            self.stats["เปิด"] += 1
            print("  -> สั่งการฮาร์ดแวร์: [เปิดไฟส่องสว่าง] สัญญาณ Relay Pin 7 = HIGH (เปิดทำงาน)")
        elif cmd in ["close", "ปิด"]:
            self.hardware_state["lamp_relay"] = False
            self.stats["ปิด"] += 1
            print("  -> สั่งการฮาร์ดแวร์: [ปิดไฟส่องสว่าง] สัญญาณ Relay Pin 7 = LOW (ปิดทำงาน)")
        elif cmd in ["red", "แดง"]:
            self.hardware_state["led_red"] = True
            self.hardware_state["led_green"] = False
            self.stats["แดง"] += 1
            print("  -> สั่งการฮาร์ดแวร์: [เปิดไฟเตือนสีแดง] LED RED Pin 8 = ON | LED GREEN Pin 9 = OFF")
        elif cmd in ["green", "เขียว"]:
            self.hardware_state["led_green"] = True
            self.hardware_state["led_red"] = False
            self.stats["เขียว"] += 1
            print("  -> สั่งการฮาร์ดแวร์: [เปิดไฟสถานะสีเขียว] LED GREEN Pin 9 = ON | LED RED Pin 8 = OFF")
        elif cmd in ["unknown", "noise"]:
            self.stats[cmd] = self.stats.get(cmd, 0) + 1
            print("  -> การคัดกรอง: ตรวจพบเสียงรบกวนหรือคำใกล้เคียงที่ไม่อยู่ในเงื่อนไข (เพิกเฉยคำสั่ง)")
        else:
            print(f"  -> คำสั่งนอกเหนือรายการที่รองรับ: '{cmd}'")

        # แสดงสถานะฮาร์ดแวร์ปัจจุบัน
        relay_text = "ON" if self.hardware_state['lamp_relay'] else "OFF"
        red_text = "ON" if self.hardware_state['led_red'] else "OFF"
        green_text = "ON" if self.hardware_state['led_green'] else "OFF"
        print(f"     [สถานะปัจจุบัน] Relay: {relay_text} | LED แดง: {red_text} | LED เขียว: {green_text}")


def run_simulation():
    """ฟังก์ชันทดสอบการทำงานของระบบในโหมดจำลองคอนโซล"""
    print("=" * 72)
    print("   ระบบรู้จำคำสั่งเสียงภาษาไทยผ่านไมโครโฟน (Thai Keyword Spotting)")
    print("   หลักสูตร: การพัฒนาปัญญาประดิษฐ์บนอุปกรณ์ขอบ (บทเรียนที่ 11)")
    print("=" * 72)
    print("[*] เริ่มต้นการทดสอบในโหมดจำลองสถานการณ์คอนโซล (Console Simulation)...")
    print("[*] คำสั่งเป้าหมายที่รองรับ: 'เปิด', 'ปิด', 'แดง', 'เขียว'")
    print("[*] กำหนดค่าเกณฑ์ความเชื่อมั่น (Confidence Threshold): 0.85 (85%)")
    print("[*] ระยะเวลาหน่วงป้องกันคำสั่งซ้ำ (Debounce Time): 2.0 วินาที")
    print("-" * 72)

    commander = ThaiVoiceCommander(confidence_threshold=0.85, debounce_sec=2.0)

    # จำลองลำดับเหตุการณ์การสั่งงานด้วยเสียง 6 เหตุการณ์
    test_voice_events = [
        ("เปิด", 0.94),
        ("แดง", 0.91),
        ("unknown", 0.88),  # คำใกล้เคียง เช่น "แดน" หรือ "แทง"
        ("เขียว", 0.92),
        ("ปิด", 0.95),
        ("ปิด", 0.92)       # จำลองการพูดซ้ำทันที (ควรติด Debounce Lock)
    ]

    for idx, (label, conf) in enumerate(test_voice_events, 1):
        print(f"\n--- [รอบการทดสอบสัญญาณเสียงที่ {idx} / {len(test_voice_events)}] ---")
        commander.execute_command(label, confidence=conf)
        time.sleep(0.15)

    print("\n" + "=" * 72)
    print("   สรุปสถิติผลการตรวจจับคำสั่งเสียงภาษาไทย")
    print("=" * 72)
    for cmd_name, count in commander.stats.items():
        print(f"  - คำสั่ง '{cmd_name:<8}': {count:>2} ครั้ง")
    print("=" * 72)
    print("[✓] การทดสอบระบบรู้จำคำสั่งเสียงภาษาไทยเสร็จสมบูรณ์ พร้อมเชื่อมต่อไมโครโฟนจริง\n")


def main():
    if not IS_ARDUINO_ENV:
        run_simulation()
        return

    print("[*] ตรวจพบสภาพแวดล้อมบอร์ดพัฒนา Arduino UNO Q พร้อมใช้งาน")
    spotter = KeywordSpotting(confidence=0.85, debounce_sec=2.0)
    commander = ThaiVoiceCommander(confidence_threshold=0.85, debounce_sec=2.0)
    time.sleep(1.0)

    info = spotter.get_model_info()
    if info is not None:
        print(f"[-] คลาสคำสั่งที่โหลดจากโมเดล: {info.labels}")
        for label in info.labels:
            def make_callback(l):
                def callback():
                    commander.execute_command(l, confidence=0.90)
                return callback
            spotter.on_detect(label, make_callback(label))

    print("[*] ระบบพร้อมรับคำสั่งเสียงภาษาไทยผ่านไมโครโฟน กด Ctrl+C เพื่อออก...")
    App.run()


if __name__ == "__main__":
    main()

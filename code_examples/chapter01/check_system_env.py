#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
รายวิชาเพิ่มเติม: ปัญญาประดิษฐ์บนระบบสมองกลฝังตัว (Embedded Artificial Intelligence)
บทเรียนที่ 1: เริ่มต้นใช้งาน Edge Impulse เพื่อเทรนโมเดล AI
สคริปต์: ตรวจสอบสภาพแวดล้อมของระบบปฏิบัติการและฮาร์ดแวร์บอร์ด Arduino UNO Q (Linux AArch64)

คำอธิบาย:
    สคริปต์นี้ทำหน้าที่ตรวจสอบความพร้อมของสภาพแวดล้อมระบบปฏิบัติการลีนุกซ์บนชิป Qualcomm Dragonwing QRB2210
    สถาปัตยกรรมซีพียู ตรวจสอบความพร้อมของหน่วยความจำ และตรวจสอบไดเรกทอรีสำหรับจัดเก็บแบบจำลอง
    ปัญญาประดิษฐ์ (.eim) เพื่อเตรียมความพร้อมก่อนเริ่มวงจรการพัฒนาโมเดล AI บน Edge Impulse
"""

import os
import sys
import platform
import subprocess

# กำหนดค่ามาตรฐานการแสดงผลข้อความภาษาไทยให้รองรับทั้ง Windows และ Linux
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def inspect_hardware_environment():
    """ตรวจสอบสถาปัตยกรรมฮาร์ดแวร์และระบบปฏิบัติการ"""
    print("=" * 65)
    print(" รายงานการตรวจสอบสภาพแวดล้อมระบบบอร์ด Arduino UNO Q (Edge AI)")
    print("=" * 65)
    
    # 1. ข้อมูลระบบปฏิบัติการและสถาปัตยกรรมซีพียู
    os_name = platform.system()
    os_release = platform.release()
    arch = platform.machine()
    python_ver = platform.python_version()
    
    print(f"[*] ระบบปฏิบัติการ (OS):             {os_name} {os_release}")
    print(f"[*] สถาปัตยกรรมหน่วยประมวลผล (Arch): {arch}")
    print(f"[*] เวอร์ชันของตัวแปลภาษาไพทอน:     Python {python_ver}")
    
    # ตรวจสอบว่าตรงกับสถาปัตยกรรมเป้าหมาย Linux AArch64 หรือไม่
    if "aarch64" in arch.lower() or "arm64" in arch.lower():
        print("    -> ผลการตรวจสอบ: รองรับไฟล์คอมไพล์เนทีฟ .eim (Linux AArch64) สมบูรณ์")
    else:
        print(f"    -> ข้อสังเกต: กำลังประมวลผลบนสถาปัตยกรรม {arch} (สำหรับการจำลอง/พัฒนาเบื้องต้น)")

def inspect_ei_model_directory():
    """ตรวจสอบไดเรกทอรีจัดเก็บแบบจำลองมาตรฐานของ Arduino Bricks"""
    ei_models_path = os.path.expanduser("~/.arduino-bricks/ei-models")
    print("\n" + "-" * 65)
    print(f"[*] ตรวจสอบไดเรกทอรีจัดเก็บไฟล์โมเดล: {ei_models_path}")
    
    if os.path.exists(ei_models_path):
        print("    -> สถานะไดเรกทอรี: พบไดเรกทอรีพร้อมใช้งาน")
        files = os.listdir(ei_models_path)
        eim_files = [f for f in files if f.endswith(".eim")]
        print(f"    -> จำนวนไฟล์โมเดล .eim ที่พบในระบบ: {len(eim_files)} ไฟล์")
        for f in eim_files:
            file_path = os.path.join(ei_models_path, f)
            size_mb = os.path.getsize(file_path) / (1024 * 1024)
            is_exec = os.access(file_path, os.X_OK)
            perm_str = "Executable (-rwxr-xr-x)" if is_exec else "Non-executable (ต้องรัน chmod +x)"
            print(f"       - {f:<25} ขนาด: {size_mb:.2f} MB | สิทธิ์: {perm_str}")
    else:
        print("    -> ไม่พบไดเรกทอรีดังกล่าวในระบบ กำลังดำเนินการสร้างไดเรกทอรี...")
        try:
            os.makedirs(ei_models_path, exist_ok=True)
            print(f"    -> สร้างไดเรกทอรีสำเร็จ: {ei_models_path}")
        except Exception as e:
            print(f"    -> เกิดข้อผิดพลาดในการสร้างไดเรกทอรี: {e}")

def inspect_edge_impulse_tools():
    """ตรวจสอบเครื่องมือ Edge Impulse CLI บนระบบ"""
    print("\n" + "-" * 65)
    print("[*] ตรวจสอบเครื่องมือ Edge Impulse Command Line Interface")
    
    tools = ["edge-impulse-linux", "edge-impulse-daemon", "edge-impulse-linux-runner"]
    for tool in tools:
        try:
            result = subprocess.run([tool, "--version"], capture_output=True, text=True, check=False)
            if result.returncode == 0:
                print(f"    -> {tool:<28}: ติดตั้งแล้ว (เวอร์ชัน {result.stdout.strip()})")
            else:
                print(f"    -> {tool:<28}: ไม่พบในระบบ (สามารถติดตั้งผ่าน npm install -g edge-impulse-linux)")
        except FileNotFoundError:
            print(f"    -> {tool:<28}: ยังไม่ได้ติดตั้งในสภาพแวดล้อมนี้")

if __name__ == "__main__":
    inspect_hardware_environment()
    inspect_ei_model_directory()
    inspect_edge_impulse_tools()
    print("\n" + "=" * 65)
    print(" สิ้นสุดการตรวจสอบความพร้อมของระบบ")
    print("=" * 65)

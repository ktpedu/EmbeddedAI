#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
รายวิชาเพิ่มเติม: ปัญญาประดิษฐ์บนระบบสมองกลฝังตัว (Embedded Artificial Intelligence)
บทเรียนที่ 5: กระบวนการ Deploy ไฟล์โมเดล (.eim) สู่บอร์ด Arduino UNO Q
สคริปต์: ยูทิลิตีช่วยตรวจสอบและติดตั้งไฟล์แบบจำลอง .eim สู่ไดเรกทอรีของระบบ

คำอธิบาย:
    สคริปต์นี้จำลองและช่วยอำนวยความสะดวกในการตรวจสอบไฟล์โมเดลไบนารี .eim
    การตรวจสอบสิทธิ์การประมวลผล (Executable Permission: chmod +x)
    และการคัดลอกไฟล์ไปยังไดเรกทอรีมาตรฐาน /home/arduino/.arduino-bricks/ei-models/
"""

import os
import sys
import shutil
import stat

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

TARGET_MODELS_DIR = os.path.expanduser("~/.arduino-bricks/ei-models")

def verify_and_deploy_model(source_eim_path: str, model_alias: str = None):
    """
    ตรวจสอบความสมบูรณ์และติดตั้งไฟล์โมเดล .eim
    """
    print("=" * 65)
    print(" ยูทิลิตีการติดตั้งไฟล์แบบจำลอง Edge Impulse (.eim) บนบอร์ด UNO Q")
    print("=" * 65)
    
    if not os.path.exists(source_eim_path):
        print(f"[!] ข้อผิดพลาด: ไม่พบไฟล์ต้นทางที่ตำแหน่ง '{source_eim_path}'")
        return False
        
    if not source_eim_path.endswith(".eim"):
        print(f"[!] คำเตือน: ไฟล์ดังกล่าวไม่ได้ลงท้ายด้วยนามสกุล '.eim'")
        
    filename = model_alias if model_alias else os.path.basename(source_eim_path)
    os.makedirs(TARGET_MODELS_DIR, exist_ok=True)
    destination_path = os.path.join(TARGET_MODELS_DIR, filename)
    
    print(f"[*] ไฟล์โมเดลต้นทาง:    {source_eim_path}")
    print(f"[*] ไดเรกทอรีปลายทาง:   {destination_path}")
    
    # 1. คัดลอกไฟล์
    shutil.copy2(source_eim_path, destination_path)
    print("    -> คัดลอกไฟล์เข้าสู่ระบบสำเร็จ")
    
    # 2. ตั้งค่าสิทธิ์ Executable (เทียบเท่าคำสั่ง chmod +x)
    current_mode = os.stat(destination_path).st_mode
    os.chmod(destination_path, current_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    print("    -> กำหนดสิทธิ์ Executable (-rwxr-xr-x) เรียบร้อยแล้ว (ป้องกัน Permission denied)")
    
    # 3. แสดงขนาดไฟล์และการตั้งค่าใน app.yaml
    size_mb = os.path.getsize(destination_path) / (1024 * 1024)
    print(f"    -> ขนาดไฟล์ไบนารี: {size_mb:.2f} MB")
    
    print("\n" + "-" * 65)
    print("[*] ตัวอย่างไวยากรณ์สำหรับไฟล์ app.yaml ที่ต้องใช้คู่กับโมเดลนี้:")
    print("-----------------------------------------------------------------")
    print("variables: {")
    print(f'  EI_V_ANOMALY_DETECTION_MODEL: "{destination_path}"')
    print("}")
    print("-----------------------------------------------------------------")
    print("=" * 65)
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1:
        verify_and_deploy_model(sys.argv[1])
    else:
        print("[คำแนะนำการใช้งาน]")
        print("  python3 deploy_eim_model.py <path-to-model.eim>")
        print("\n[การจำลองระบบ]: กำลังตรวจสอบโครงสร้างไดเรกทอรีปลายทาง...")
        print(f"  เป้าหมาย: {TARGET_MODELS_DIR}")
        os.makedirs(TARGET_MODELS_DIR, exist_ok=True)
        print("  สถานะไดเรกทอรี: พร้อมรับไฟล์โมเดลจาก Edge Impulse")

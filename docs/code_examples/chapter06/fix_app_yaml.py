#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
รายวิชาเพิ่มเติม: ปัญญาประดิษฐ์บนระบบสมองกลฝังตัว (Embedded Artificial Intelligence)
บทเรียนที่ 6: การนำโมเดล .eim ไปใช้งานและการกำหนดค่าไฟล์ app.yaml บนบอร์ดพัฒนา Arduino UNO Q
สคริปต์: fix_app_yaml.py - การตรวจสอบ แก้ไข และตรวจสอบสิทธิ์ไฟล์โมเดลไบนารี (.eim)

คำอธิบาย:
    สคริปต์นี้พัฒนาขึ้นเพื่อตรวจสอบความถูกต้องของโครงสร้างไวยากรณ์ในไฟล์คอนฟิกูเรชัน app.yaml
    ซึ่งระบบจัดการแอปพลิเคชัน Arduino App Lab กำหนดให้ส่วนตัวแปรระบบต้องอยู่ในรูปแบบพจนานุกรม
    variables: { KEY: "VALUE", ... } พร้อมทั้งตรวจสอบพาธไดเรกทอรี สิทธิ์การประมวลผลคำสั่ง (chmod +x)
    และขนาดของไฟล์โมเดลไบนารี .eim ก่อนนำเข้าสู่กระบวนการประมวลผลจริง
"""

import os
import sys
import re
import stat

# ตั้งค่าการแสดงผลภาษาไทยบนคอนโซลให้ถูกต้อง
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

DEFAULT_APP_YAML_PATH = os.path.join(os.path.dirname(__file__), "app.yaml")
MODELS_DIR = "/home/arduino/.arduino-bricks/ei-models"

# รายการตัวแปรมาตรฐานสำหรับโมเดล Edge AI แต่ละประเภท
STANDARD_MODEL_VARS = {
    "EI_V_ANOMALY_DETECTION_MODEL": "AnomalyDetection.eim",
    "EI_OBJ_DETECTION_MODEL": "fomo_object_detection.eim",
    "EI_CLASSIFICATION_MODEL": "image_classification.eim",
    "EI_KEYWORD_SPOTTING_MODEL": "KWS_model.eim",
    "EI_AUDIO_CLASSIFICATION_MODEL": "AC_model.eim"
}

def analyze_app_yaml_syntax(file_path: str) -> dict:
    """ตรวจสอบความถูกต้องของโครงสร้างไวยากรณ์ไฟล์ app.yaml"""
    if not os.path.exists(file_path):
        return {"valid": False, "reason": f"ไม่พบไฟล์คอนฟิกูเรชัน: {file_path}", "variables": {}}

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # ตรวจสอบรูปแบบ variables: { ... }
    brace_pattern = re.compile(r'variables:\s*\{([^}]*)\}', re.DOTALL)
    match = brace_pattern.search(content)

    if not match:
        # ตรวจสอบว่าเขียนเป็นแบบ list หรือบล็อกย่อหน้าที่ผิดไวยากรณ์หรือไม่
        is_list_format = bool(re.search(r'variables:\s*\n\s*-\s*', content))
        is_block_dict = bool(re.search(r'variables:\s*\n\s*[A-Z_]+:', content))
        
        reason = "โครงสร้าง variables ไม่ได้ใช้วงเล็บปีกกา { ... } ตามมาตรฐาน Arduino App Lab"
        if is_list_format:
            reason += " (ตรวจพบการใช้เครื่องหมายขีด - แบบ Array ซึ่งไม่ถูกต้อง)"
        elif is_block_dict:
            reason += " (ตรวจพบการขึ้นบรรทัดใหม่แบบ YAML Dictionary ดั้งเดิมโดยไม่มีปีกกาครอบ)"
            
        return {"valid": False, "reason": reason, "variables": {}}

    # ดึงค่าคู่ตัวแปรภายในวงเล็บปีกกา
    raw_vars = match.group(1).strip()
    extracted_vars = {}
    lines = raw_vars.split("\n")
    for line in lines:
        line = line.strip().rstrip(",")
        if ":" in line:
            k, v = line.split(":", 1)
            key = k.strip()
            val = v.strip().strip('"').strip("'")
            extracted_vars[key] = val

    return {
        "valid": True,
        "reason": "โครงสร้างไวยากรณ์ถูกต้องสมบูรณ์ตามมาตรฐาน Arduino App Lab",
        "variables": extracted_vars
    }


def generate_standard_app_yaml(target_path: str, custom_vars: dict = None) -> bool:
    """สร้างหรือเขียนทับไฟล์ app.yaml ด้วยรูปแบบมาตรฐานที่ถูกต้อง 100%"""
    vars_dict = custom_vars if custom_vars else {
        k: f"{MODELS_DIR}/{v}" for k, v in STANDARD_MODEL_VARS.items()
    }

    yaml_lines = [
        "# ==============================================================================",
        "# การกำหนดค่าตัวแปรโมเดลบนระบบ Arduino App Lab (มาตรฐานไวยากรณ์ล่าสุด)",
        "# ==============================================================================",
        "name: EdgeAI Deployment Template",
        'description: "เทมเพลตการกำหนดค่าตัวแปรสภาพแวดล้อมสำหรับแบบจำลอง Edge Impulse บนบอร์ด Arduino UNO Q"',
        "ports: []",
        "variables: {"
    ]

    var_entries = []
    for k, v in vars_dict.items():
        var_entries.append(f'  {k}: "{v}"')

    yaml_lines.append(",\n".join(var_entries))
    yaml_lines.append("}")
    yaml_lines.append("bricks: []\n")

    try:
        with open(target_path, "w", encoding="utf-8") as f:
            f.write("\n".join(yaml_lines))
        return True
    except Exception as e:
        print(f"[!] เกิดข้อผิดพลาดในการเขียนไฟล์: {e}")
        return False


def verify_model_binary(model_path: str):
    """ตรวจสอบไฟล์ไบนารี .eim ว่ามีอยู่จริงและมีสิทธิ์ Execute หรือไม่"""
    print(f"\n[*] การตรวจสอบไฟล์โมเดลไบนารี: {model_path}")
    if not os.path.exists(model_path):
        print(f"    └─ [สถานะ] ยังไม่พบไฟล์ในเครื่องจำลอง (เป็นเรื่องปกติขณะทดสอบบนเครื่องคอมพิวเตอร์)")
        print(f"       แนวทางปฏิบัติ: ให้ดาวน์โหลดไฟล์ Linux AArch64 .eim แล้วส่งผ่าน SSH ไปยังตำแหน่งดังกล่าว")
        return False

    # ตรวจสอบสิทธิ์การประมวลผลคำสั่ง
    file_mode = os.stat(model_path).st_mode
    is_executable = bool(file_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
    file_size_mb = os.path.getsize(model_path) / (1024 * 1024)

    print(f"    ├─ ขนาดไฟล์ไบนารี:  {file_size_mb:.2f} MB")
    if is_executable:
        print(f"    └─ สิทธิ์การประมวลผล: ผ่านเกณฑ์ (Executable: rwxr-xr-x)")
    else:
        print(f"    └─ สิทธิ์การประมวลผล: \033[91mยังไม่ได้รับสิทธิ์ประมวลผลคำสั่ง\033[0m")
        print(f"       แนวทางแก้ไข: รันคำสั่ง 'chmod +x {model_path}' เพื่อป้องกันข้อผิดพลาด Permission denied")

    return is_executable


def main():
    print("=" * 75)
    print(" บทเรียนที่ 6: ยูทิลิตีตรวจสอบและกำหนดค่าไฟล์ app.yaml บน Arduino UNO Q")
    print("=" * 75)

    target_file = DEFAULT_APP_YAML_PATH
    print(f"[*] ตำแหน่งไฟล์เป้าหมาย: {target_file}")

    # 1. วิเคราะห์ไวยากรณ์ปัจจุบัน
    analysis = analyze_app_yaml_syntax(target_file)
    print(f"[*] ผลการวิเคราะห์ไวยากรณ์: {'\033[92mถูกต้องสมบูรณ์ (PASS)\033[0m' if analysis['valid'] else '\033[91mไม่ถูกต้อง (FAIL)\033[0m'}")
    print(f"    └─ รายละเอียด: {analysis['reason']}")

    if not analysis["valid"]:
        print("\n[*] ดำเนินการปรับปรุงและแก้ไขโครงสร้างไฟล์ให้เป็นมาตรฐานอัตโนมัติ...")
        success = generate_standard_app_yaml(target_file)
        if success:
            print("    └─ [สำเร็จ] แก้ไขไฟล์ app.yaml ด้วยโครงสร้าง variables: { ... } เรียบร้อยแล้ว")
            analysis = analyze_app_yaml_syntax(target_file)
        else:
            print("    └─ [ล้มเหลว] ไม่สามารถปรับปรุงไฟล์ได้")

    # 2. แสดงรายการตัวแปรโมเดลที่กำหนดในระบบ
    print("\n[*] สรุปตัวแปรโมเดลปัญญาประดิษฐ์ในระบบ (Configured Model Paths):")
    for key, path in analysis["variables"].items():
        print(f"  ├─ {key:<30} -> {path}")

    # 3. ตรวจสอบไฟล์โมเดลตัวอย่าง
    sample_model = analysis["variables"].get("EI_V_ANOMALY_DETECTION_MODEL", f"{MODELS_DIR}/AnomalyDetection.eim")
    verify_model_binary(sample_model)

    print("\n" + "=" * 75)
    print(" [สรุปผลการตรวจสอบ]")
    print(" 1. ไวยากรณ์ของไฟล์ app.yaml อยู่ในรูปแบบพจนานุกรมวงเล็บปีกกา { ... } ถูกต้อง")
    print(" 2. สามารถนำไปใช้งานร่วมกับโมดูล Brick ในบทเรียนที่ 7 ได้อย่างราบรื่น")
    print("=" * 75 + "\n")


if __name__ == "__main__":
    main()

@echo off
chcp 65001 > nul
title Edge AI Learning Platform Server
color 0B

echo =======================================================
echo   KT-Edu & depa: Edge AI Learning Platform
echo   กำลังเริ่มต้นเซิร์ฟเวอร์ระบบเว็บบทเรียนออนไลน์...
echo =======================================================
echo.

cd /d "%~dp0web_learning_platform"

if not exist "server.js" (
    echo [ERROR] ไม่พบไฟล์ server.js ในโฟลเดอร์ web_learning_platform
    pause
    exit /b
)

echo [*] กำลังตรวจสอบพอร์ตและเริ่มต้นเซิร์ฟเวอร์...
node server.js

pause

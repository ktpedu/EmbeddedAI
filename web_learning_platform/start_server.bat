@echo off
chcp 65001 > nul
title Edge AI Learning Platform Server
color 0B

echo =======================================================
echo   KT-Edu & depa: Edge AI Learning Platform
echo   กำลังเริ่มต้นเซิร์ฟเวอร์ระบบเว็บบทเรียนออนไลน์...
echo =======================================================
echo.

cd /d "%~dp0"

echo [*] เริ่มต้นเซิร์ฟเวอร์ที่: http://localhost:3000
echo [*] กำลังเปิดเว็บเบราว์เซอร์อัตโนมัติ...
start http://localhost:3000

echo.
echo กด Ctrl + C ในหน้าต่างนี้เพื่อหยุดการทำงานของเซิร์ฟเวอร์
echo =======================================================
echo.

node server.js

pause

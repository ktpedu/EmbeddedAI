@echo off
cd /d "%~dp0"
echo ========================================================
echo   Updating EdgeAI to GitHub: ktpedu/EmbeddedAI
echo ========================================================
echo.
git push origin main
echo.
if %ERRORLEVEL% EQU 0 (
    echo ========================================================
    echo  SUCCESS! Updated to https://github.com/ktpedu/EmbeddedAI
    echo ========================================================
) else (
    echo ========================================================
    echo  Push failed. If needed, sign in via browser or token.
    echo ========================================================
)
echo.
pause

@echo off
cd /d "%~dp0"
echo ========================================================
echo   Uploading EdgeAI to GitHub: ktpedu/EmbeddedAI
echo ========================================================
echo.
echo [1/3] Clearing old saved GitHub account (wny-ict)...
cmdkey /delete:git:https://github.com >nul 2>&1
cmdkey /delete:LegacyGeneric:target=git:https://github.com >nul 2>&1

echo.
echo [2/3] Setting remote target to ktpedu/EmbeddedAI...
git remote set-url origin https://ktpedu@github.com/ktpedu/EmbeddedAI.git

echo.
echo [3/3] Uploading 1,962 files to GitHub...
echo.
echo ********************************************************
echo  IMPORTANT:
echo  A GitHub login window will pop up in your browser.
echo  Please click "Sign in with your browser"
echo  and confirm with your "ktpedu" account!
echo ********************************************************
echo.
git push -u origin main
echo.
if %ERRORLEVEL% EQU 0 (
    echo ========================================================
    echo  SUCCESS! Uploaded to https://github.com/ktpedu/EmbeddedAI
    echo ========================================================
) else (
    echo ========================================================
    echo  If it still shows denied, remove 'git:https://github.com'
    echo  from Windows Credential Manager.
    echo ========================================================
)
echo.
pause

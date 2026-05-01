@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo.
echo ============================================================
echo   BrillianceLab - Quick deploy (commit + push)
echo ============================================================
echo.

REM Verify repo exists
if not exist ".git" (
    echo This folder is not a git repo yet. Run setup.bat first.
    echo.
    pause
    exit /b 1
)

REM Verify remote
for /f "tokens=*" %%u in ('git config --get remote.origin.url 2^>nul') do set "REMOTE_URL=%%u"
if "!REMOTE_URL!"=="" (
    echo No remote 'origin' configured. Run setup.bat first.
    echo.
    pause
    exit /b 1
)

set /p MSG="Commit message (Enter to use default): "
if "!MSG!"=="" set "MSG=Update site"

echo.
git add -A
git diff --cached --quiet
if errorlevel 1 (
    git commit -m "!MSG!"
) else (
    echo No staged changes - skipping commit.
)
git push
if errorlevel 1 (
    echo.
    echo [WARN] Push failed. If remote has commits you don't, try:
    echo        git pull --rebase origin main
    echo        then re-run deploy.bat
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   Done. Remote:    !REMOTE_URL!
echo   Vercel will auto-deploy in ~30 seconds.
echo   Live URL:        https://brilliancelab.vercel.app/
echo ============================================================
echo.
pause
endlocal

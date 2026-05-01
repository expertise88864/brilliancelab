@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo ============================================================
echo   BrillianceLab - Deploy update to GitHub / Vercel
echo ============================================================
echo.

set /p msg="Commit message (Enter to use default): "
if "%msg%"=="" set msg=Update site

git add -A
git commit -m "%msg%"
git push

echo.
echo ============================================================
echo   Done. Vercel will auto-deploy in ~30 seconds.
echo   Live URL: https://brilliancelab.vercel.app/
echo ============================================================
echo.
pause

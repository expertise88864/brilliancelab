@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo ============================================================
echo   BrillianceLab - GitHub setup
echo ============================================================
echo.

echo [1/5] Setting git identity (global)...
git config --global user.email "expertise88864@users.noreply.github.com"
git config --global user.name  "expertise88864"

echo.
echo [2/5] Verifying identity...
for /f "tokens=*" %%a in ('git config --global user.email') do echo     email = %%a
for /f "tokens=*" %%a in ('git config --global user.name')  do echo     name  = %%a

echo.
echo [3/5] Staging files...
git add -A

echo.
echo [4/5] Creating commit...
git commit -m "Initial commit: BrillianceLab landing page"

echo.
echo [5/5] Pushing to GitHub (origin/main)...
git branch -M main
git push -u origin main

echo.
echo ============================================================
echo   Done. If a browser popped up, complete GitHub login.
echo ============================================================
echo.
pause

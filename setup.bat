@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo.
echo ============================================================
echo   BrillianceLab - One-click Push to GitHub
echo ============================================================
echo   Working dir: %CD%
echo.

REM --- 0) Check git is installed ---
where git >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git is not installed or not on PATH.
    echo         Install from https://git-scm.com/download/win then re-run.
    echo.
    pause
    exit /b 1
)

REM --- 1) Set git identity (only if not already set) ---
echo [1/6] Verifying git identity...
for /f "tokens=*" %%a in ('git config --global user.email 2^>nul') do set "GIT_EMAIL=%%a"
for /f "tokens=*" %%a in ('git config --global user.name  2^>nul') do set "GIT_NAME=%%a"
if "!GIT_EMAIL!"=="" (
    git config --global user.email "expertise88864@users.noreply.github.com"
    set "GIT_EMAIL=expertise88864@users.noreply.github.com"
)
if "!GIT_NAME!"=="" (
    git config --global user.name  "expertise88864"
    set "GIT_NAME=expertise88864"
)
echo     email = !GIT_EMAIL!
echo     name  = !GIT_NAME!

REM --- 2) Init repo if needed ---
echo.
echo [2/6] Repo state...
if not exist ".git" (
    echo     No .git found - initializing new repo
    git init
    git branch -M main
) else (
    echo     Existing repo OK
)

REM --- 3) Make sure 'main' is the active branch ---
for /f "tokens=*" %%b in ('git rev-parse --abbrev-ref HEAD 2^>nul') do set "CUR_BR=%%b"
if not "!CUR_BR!"=="main" (
    echo     Switching branch to main
    git branch -M main
)

REM --- 4) Ensure remote 'origin' exists ---
echo.
echo [3/6] Checking remote 'origin'...
for /f "tokens=*" %%u in ('git config --get remote.origin.url 2^>nul') do set "REMOTE_URL=%%u"
if "!REMOTE_URL!"=="" (
    echo     No remote 'origin' configured.
    echo.
    echo     Paste your GitHub repo URL ^(e.g. https://github.com/USER/REPO.git^):
    set /p REMOTE_URL="    URL: "
    if "!REMOTE_URL!"=="" (
        echo [ERROR] No URL given. Aborting.
        pause
        exit /b 1
    )
    git remote add origin "!REMOTE_URL!"
    if errorlevel 1 (
        echo [ERROR] Failed to add remote. Aborting.
        pause
        exit /b 1
    )
    echo     Remote set to !REMOTE_URL!
) else (
    echo     origin = !REMOTE_URL!
)

REM --- 5) Stage everything (except .git, node_modules, etc — covered by .gitignore if present) ---
echo.
echo [4/6] Staging files...
git add -A

REM --- 6) Decide if there's anything to commit ---
git diff --cached --quiet
if errorlevel 1 (
    REM There ARE staged changes
    set /p MSG="    Commit message (Enter to use default 'Update site'): "
    if "!MSG!"=="" set "MSG=Update site"
    echo.
    echo [5/6] Creating commit: !MSG!
    git commit -m "!MSG!"
    if errorlevel 1 (
        echo [ERROR] Commit failed. See message above.
        pause
        exit /b 1
    )
) else (
    echo.
    echo [5/6] No staged changes - nothing to commit.
    echo       Will still attempt to push in case local commits are ahead of remote.
)

REM --- 7) Push (with -u on first push) ---
echo.
echo [6/6] Pushing to GitHub (origin/main)...
git push -u origin main
if errorlevel 1 (
    echo.
    echo [WARN] Push failed. Common causes:
    echo        - First push: a browser popup may have appeared. Complete login and re-run.
    echo        - Remote already has commits you don't: try
    echo            git pull --rebase origin main
    echo          then re-run setup.bat
    echo        - Wrong remote URL: edit it with
    echo            git remote set-url origin https://github.com/USER/REPO.git
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   Done!
echo   Remote:    !REMOTE_URL!
echo   Branch:    main
echo   Live URL:  https://brilliancelab.vercel.app/
echo.
echo   Vercel will auto-deploy in ~30 seconds if connected.
echo ============================================================
echo.
pause
endlocal

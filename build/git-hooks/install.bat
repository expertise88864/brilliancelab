@echo off
REM Install BrillianceLab git hooks (Windows). Run once after cloning.
setlocal
cd /d "%~dp0..\.."

if not exist ".git\hooks" mkdir ".git\hooks"
copy /Y build\git-hooks\pre-commit .git\hooks\pre-commit >nul
echo [ok] pre-commit hook installed at .git\hooks\pre-commit
echo      runs: JSON-LD parse · canonical audit · check_js · punct dry-run
echo      bypass once with:  git commit --no-verify
echo.
echo [note] Git for Windows runs hooks via the bundled bash, so no extra
echo        chmod is needed; the shebang line is enough.
endlocal

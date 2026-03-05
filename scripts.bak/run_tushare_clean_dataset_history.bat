@echo off
setlocal

:: Get the directory of the script and change to project root (one level up)
cd /d "%~dp0.."
set "PROJECT_ROOT=%CD%"

:: Activate the env
call conda activate %PROJECT_ROOT%\venv\tushare

:: Loop from 2012 to 2026 with a step of 1
FOR /L %%y IN (2012, 1, 2026) DO (
    echo [LOG] Processing year: %%y
    python -m src.vendors.tushare.cli clean dataset --year %%y --replace True
)
echo Done for ALL YEARs!
pause

endlocal
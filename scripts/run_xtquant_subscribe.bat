@echo off
setlocal

:: ------------------------------------------------------------------------------
:: Prepare the directory and venv
:: Get the directory of the script and change to project root (one level up)
cd /d "%~dp0.."
set "PROJECT_ROOT=%CD%"
call conda activate %PROJECT_ROOT%\venv\xt
:: ------------------------------------------------------------------------------

echo Running XTQuant pipeline - subscribe real-time quote data

:: Subscribe
echo Step: Subscribing real-time quote...
python -m src.vendors.xtquant.cli subscribe realtime-quote


endlocal
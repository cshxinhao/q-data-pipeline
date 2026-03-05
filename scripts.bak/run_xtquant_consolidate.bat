@echo off
setlocal

:: Preparation
cd /d "%~dp0.."
set "PROJECT_ROOT=%CD%"
call conda activate %PROJECT_ROOT%\venv\xt

:: Set params
:: Set date range for demonstration
for /f %%a in ('powershell -Command "Get-Date -Format yyyy-MM-dd"') do set TODAY=%%a
echo Today is %TODAY%

echo Running XTQuant pipeline - consolidating from %PROJECT_ROOT%

:: Clean

echo Step: Consolidating realtime quote...
python -m src.vendors.xtquant.cli clean realtime-quote --date %TODAY%


echo XTQuant pipeline - consolidating completed.

endlocal
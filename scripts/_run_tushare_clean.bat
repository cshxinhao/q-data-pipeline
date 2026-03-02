@echo off
setlocal

:: Get the directory of the script and change to project root (one level up)
cd /d "%~dp0.."
set "PROJECT_ROOT=%CD%"

set "replace=True"

:: Set date range for demonstration
set "START_DATE=20120101"
::set "START_DATE=20260227"
set "END_DATE=20260228"

echo Running Tushare pipeline - clean from %PROJECT_ROOT%

:: Activate the env
call conda activate %PROJECT_ROOT%\venv\tushare


:: Clean

echo Step: Cleaning trade calendar...
python -m src.vendors.tushare.cli clean trade-cal

echo Step: Cleaning identity...
python -m src.vendors.tushare.cli clean identity

echo Step: Cleaning 1-day bar prices (%START_DATE% - %END_DATE%)...
python -m src.vendors.tushare.cli clean 1day-bar --start %START_DATE% --end %END_DATE% --replace %replace%

echo Step: Cleaning adj factor (%START_DATE% - %END_DATE%)...
python -m src.vendors.tushare.cli clean adj-factor --start %START_DATE% --end %END_DATE% --replace %replace%

echo Step: Cleaning basic info to cap (%START_DATE% - %END_DATE%)...
python -m src.vendors.tushare.cli clean cap --start %START_DATE% --end %END_DATE% --replace %replace%

echo Step: Cleaning basic info to valuation (%START_DATE% - %END_DATE%)...
python -m src.vendors.tushare.cli clean valuation --start %START_DATE% --end %END_DATE% --replace %replace%

echo Step: Cleaning listed days...
python -m src.vendors.tushare.cli clean listed-days


echo Tushare pipeline - clean completed.

endlocal
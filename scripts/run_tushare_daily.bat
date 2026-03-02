@echo off
setlocal

:: Get the directory of the script and change to project root (one level up)
cd /d "%~dp0.."
set "PROJECT_ROOT=%CD%"

set "replace=True"

:: Set date range for demonstration
for /f %%a in ('powershell -Command "Get-Date -Format yyyy-MM-dd"') do set TODAY=%%a
echo %TODAY%
set "START_DATE=%TODAY%"
set "END_DATE=%TODAY%"

echo Running Tushare pipeline from %PROJECT_ROOT%

:: Activate the env
call conda activate %PROJECT_ROOT%\venv\tushare


:: Download

echo Step: Downloading trade calendar (20120101 - %END_DATE%)...
python -m src.vendors.tushare.cli download trade-cal --start 20120101 --end %END_DATE%

echo Step: Downloading ticker mapper...
python -m src.vendors.tushare.cli download ticker-mapper

echo Step: Downloading 1-day bar prices (%START_DATE% - %END_DATE%)...
python -m src.vendors.tushare.cli download 1day-bar --start %START_DATE% --end %END_DATE% --replace %replace%

echo Step: Downloading adj factor (%START_DATE% - %END_DATE%)...
python -m src.vendors.tushare.cli download adj-factor --start %START_DATE% --end %END_DATE% --replace %replace%

echo Step: Downloading basic (%START_DATE% - %END_DATE%)...
python -m src.vendors.tushare.cli download basic --start %START_DATE% --end %END_DATE% --replace %replace%


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

set "YEAR=%START_DATE:~0,4%"
echo Step: Cleaning dataset (%YEAR%)...
python -m src.vendors.tushare.cli clean dataset --year %YEAR% --replace %replace%


echo Tushare pipeline completed.

endlocal
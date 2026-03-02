@echo off
setlocal

:: Get the directory of the script and change to project root (one level up)
cd /d "%~dp0.."
set "PROJECT_ROOT=%CD%"

:: Set date range for demonstration
::set "START_DATE=20120101"
set "START_DATE=20260227"
set "END_DATE=20260228"
set "replace=False"

echo Running Tushare pipeline from %PROJECT_ROOT%

:: Activate the env
call conda activate %PROJECT_ROOT%\venv\tushare


:: 1. Trade Calendar

:: 1.1 Download Trade Calendar
echo Step 1.1: Downloading trade calendar (20120101 - %END_DATE%)...
python -m src.vendors.tushare.cli download trade-cal --start 20120101 --end %END_DATE%

:: 1.2 Clean Trade Calendar
echo Step 1.2: Cleaning trade calendar...
python -m src.vendors.tushare.cli clean trade-cal


:: 2. Ticker Mapper

:: 2.1 Download Ticker Mapper
echo Step 2.1: Downloading ticker mapper...
python -m src.vendors.tushare.cli download ticker-mapper

:: 2.2 Clean Identity
echo Step 2.2: Cleaning identity...
python -m src.vendors.tushare.cli clean identity


:: 3. 1-Day Bar Prices

:: 3.1 Download 1-Day Bar Prices
echo Step 3.1: Downloading 1-day bar prices (%START_DATE% - %END_DATE%)...
python -m src.vendors.tushare.cli download 1day-bar --start %START_DATE% --end %END_DATE% --replace %replace%

:: 3.2 Clean 1-Day Bar Prices
echo Step 3.2: Cleaning 1-day bar prices (%START_DATE% - %END_DATE%)...
python -m src.vendors.tushare.cli clean 1day-bar --start %START_DATE% --end %END_DATE% --replace %replace%


:: 4. Adj Factor

:: 4.1 Download Adj Factor
echo Step 4.1: Downloading adj factor (%START_DATE% - %END_DATE%)...
python -m src.vendors.tushare.cli download adj-factor --start %START_DATE% --end %END_DATE% --replace %replace%

:: 4.2 Clean Adj Factor
echo Step 4.2: Cleaning adj factor (%START_DATE% - %END_DATE%)...
python -m src.vendors.tushare.cli clean adj-factor --start %START_DATE% --end %END_DATE% --replace %replace%


:: 5. Basic Info

:: 5.1 Download Basic Info
echo Step 5.1: Downloading basic (%START_DATE% - %END_DATE%)...
python -m src.vendors.tushare.cli download basic --start %START_DATE% --end %END_DATE% --replace %replace%

:: 5.2 Clean Cap
echo Step 5.2: Cleaning basic info to cap (%START_DATE% - %END_DATE%)...
python -m src.vendors.tushare.cli clean cap --start %START_DATE% --end %END_DATE% --replace %replace%

:: 5.3 Clean Valuation
echo Step 5.3: Cleaning basic info to valuation (%START_DATE% - %END_DATE%)...
python -m src.vendors.tushare.cli clean valuation --start %START_DATE% --end %END_DATE% --replace %replace%

echo Tushare pipeline completed.

endlocal
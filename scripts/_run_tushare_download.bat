@echo off
setlocal

:: Get the directory of the script and change to project root (one level up)
cd /d "%~dp0.."
set "PROJECT_ROOT=%CD%"

set "replace=True"

:: Set date range for demonstration
::set "START_DATE=20120101"
set "START_DATE=20260227"
set "END_DATE=20260228"

echo Running Tushare pipeline - download from %PROJECT_ROOT%

:: Activate the env
call conda activate %PROJECT_ROOT%\venv\tushare


:: Download

echo Step: Downloading trade calendar (19900101 - %END_DATE%)...
python -m src.vendors.tushare.cli download trade-cal --start 19900101 --end %END_DATE%

echo Step: Downloading ticker mapper...
python -m src.vendors.tushare.cli download ticker-mapper

echo Step: Downloading 1-day bar prices (%START_DATE% - %END_DATE%)...
python -m src.vendors.tushare.cli download 1day-bar --start %START_DATE% --end %END_DATE% --replace %replace%

echo Step: Downloading adj factor (%START_DATE% - %END_DATE%)...
python -m src.vendors.tushare.cli download adj-factor --start %START_DATE% --end %END_DATE% --replace %replace%

echo Step: Downloading basic (%START_DATE% - %END_DATE%)...
python -m src.vendors.tushare.cli download basic --start %START_DATE% --end %END_DATE% --replace %replace%


echo Tushare pipeline - download completed.

endlocal
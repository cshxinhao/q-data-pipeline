@echo off
setlocal EnableDelayedExpansion

:: ==================================================================================
::  SCRIPT: Tushare Daily Pipeline
::  DESC:   Downloads and cleans daily Tushare data (Calendar, Mapper, Bar, Factors)
:: ==================================================================================

cd /d "%~dp0.."
set "PROJECT_ROOT=%CD%"

echo.
echo ==================================================================================
echo  [START] Tushare Daily Pipeline
echo  Time: %DATE% %TIME%
echo  Root: %PROJECT_ROOT%
echo ==================================================================================
echo.

:: ----------------------------------------------------------------------------------
::  Configuration
:: ----------------------------------------------------------------------------------
set "replace=True"

:: Get Today's Date
for /f %%a in ('powershell -Command "Get-Date -Format yyyy-MM-dd"') do set TODAY=%%a
set "START_DATE=%TODAY%"
set "END_DATE=%TODAY%"

echo [INFO] Date Range: %START_DATE% to %END_DATE%
echo [INFO] Replace:    %replace%
echo.

:: ----------------------------------------------------------------------------------
::  Environment
:: ----------------------------------------------------------------------------------
echo [INFO] Activating conda environment (tushare)...
call conda activate %PROJECT_ROOT%\venv\tushare
if %errorlevel% neq 0 (
    echo [ERROR] Failed to activate environment.
    exit /b %errorlevel%
)
echo.

:: ----------------------------------------------------------------------------------
::  Download Phase
:: ----------------------------------------------------------------------------------

echo ----------------------------------------------------------------------------------
echo [STEP] Downloading Trade Calendar (19900101 - %END_DATE%)
echo ----------------------------------------------------------------------------------
python -m src.vendors.tushare.cli download trade-cal --start 19900101 --end %END_DATE%
echo.

echo ----------------------------------------------------------------------------------
echo [STEP] Downloading Ticker Mapper
echo ----------------------------------------------------------------------------------
python -m src.vendors.tushare.cli download ticker-mapper
echo.

echo ----------------------------------------------------------------------------------
echo [STEP] Downloading 1-Day Bar Prices (%START_DATE% - %END_DATE%)
echo ----------------------------------------------------------------------------------
python -m src.vendors.tushare.cli download 1day-bar --start %START_DATE% --end %END_DATE% --replace %replace%
echo.

echo ----------------------------------------------------------------------------------
echo [STEP] Downloading Adj Factor (%START_DATE% - %END_DATE%)
echo ----------------------------------------------------------------------------------
python -m src.vendors.tushare.cli download adj-factor --start %START_DATE% --end %END_DATE% --replace %replace%
echo.

echo ----------------------------------------------------------------------------------
echo [STEP] Downloading Basic Info (%START_DATE% - %END_DATE%)
echo ----------------------------------------------------------------------------------
python -m src.vendors.tushare.cli download basic --start %START_DATE% --end %END_DATE% --replace %replace%
echo.

:: ----------------------------------------------------------------------------------
::  Clean Phase
:: ----------------------------------------------------------------------------------

echo ----------------------------------------------------------------------------------
echo [STEP] Cleaning Trade Calendar
echo ----------------------------------------------------------------------------------
python -m src.vendors.tushare.cli clean trade-cal
echo.

echo ----------------------------------------------------------------------------------
echo [STEP] Cleaning Identity
echo ----------------------------------------------------------------------------------
python -m src.vendors.tushare.cli clean identity
echo.

echo ----------------------------------------------------------------------------------
echo [STEP] Cleaning 1-Day Bar Prices (%START_DATE% - %END_DATE%)
echo ----------------------------------------------------------------------------------
python -m src.vendors.tushare.cli clean 1day-bar --start %START_DATE% --end %END_DATE% --replace %replace%
echo.

echo ----------------------------------------------------------------------------------
echo [STEP] Cleaning Adj Factor (%START_DATE% - %END_DATE%)
echo ----------------------------------------------------------------------------------
python -m src.vendors.tushare.cli clean adj-factor --start %START_DATE% --end %END_DATE% --replace %replace%
echo.

echo ----------------------------------------------------------------------------------
echo [STEP] Cleaning Basic Info to Cap (%START_DATE% - %END_DATE%)
echo ----------------------------------------------------------------------------------
python -m src.vendors.tushare.cli clean cap --start %START_DATE% --end %END_DATE% --replace %replace%
echo.

echo ----------------------------------------------------------------------------------
echo [STEP] Cleaning Basic Info to Valuation (%START_DATE% - %END_DATE%)
echo ----------------------------------------------------------------------------------
python -m src.vendors.tushare.cli clean valuation --start %START_DATE% --end %END_DATE% --replace %replace%
echo.

set "YEAR=%START_DATE:~0,4%"
echo ----------------------------------------------------------------------------------
echo [STEP] Cleaning Dataset (%YEAR%)
echo ----------------------------------------------------------------------------------
python -m src.vendors.tushare.cli clean dataset --year %YEAR% --replace %replace%
echo.

echo ==================================================================================
echo  [DONE] Tushare Daily Pipeline Completed.
echo  Time: %DATE% %TIME%
echo ==================================================================================
echo.

endlocal

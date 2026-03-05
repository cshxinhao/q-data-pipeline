@echo off
setlocal EnableDelayedExpansion

:: ==================================================================================
::  SCRIPT: Tushare Clean Pipeline
::  DESC:   Cleans downloaded Tushare data
:: ==================================================================================

cd /d "%~dp0.."
set "PROJECT_ROOT=%CD%"

echo.
echo ==================================================================================
echo  [START] Tushare Clean Pipeline
echo  Time: %DATE% %TIME%
echo  Root: %PROJECT_ROOT%
echo ==================================================================================
echo.

:: ----------------------------------------------------------------------------------
::  Configuration
:: ----------------------------------------------------------------------------------
set "replace=True"

:: Set date range (Manual Configuration)
:: set "START_DATE=20120101"
set "START_DATE=20260227"
set "END_DATE=20260228"

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

echo ----------------------------------------------------------------------------------
echo [STEP] Cleaning Listed Days
echo ----------------------------------------------------------------------------------
python -m src.vendors.tushare.cli clean listed-days
echo.

echo ==================================================================================
echo  [DONE] Tushare Clean Pipeline Completed.
echo  Time: %DATE% %TIME%
echo ==================================================================================
echo.

endlocal

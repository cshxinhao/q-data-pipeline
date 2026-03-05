@echo off
setlocal EnableDelayedExpansion

:: ==================================================================================
::  SCRIPT: XTQuant Clean Pipeline
::  DESC:   Cleans downloaded XTQuant data
:: ==================================================================================

cd /d "%~dp0.."
set "PROJECT_ROOT=%CD%"

echo.
echo ==================================================================================
echo  [START] XTQuant Clean Pipeline
echo  Time: %DATE% %TIME%
echo  Root: %PROJECT_ROOT%
echo ==================================================================================
echo.

:: ----------------------------------------------------------------------------------
::  Configuration
:: ----------------------------------------------------------------------------------
set "replace=True"

:: Set params
:: @REM set "START_DATE=20120101"
set "START_DATE=20120101"
set "END_DATE=20260304"

echo [INFO] Date Range: %START_DATE% to %END_DATE%
echo [INFO] Replace:    %replace%
echo.

:: ----------------------------------------------------------------------------------
::  Environment
:: ----------------------------------------------------------------------------------
echo [INFO] Activating conda environment (xt)...
call conda activate %PROJECT_ROOT%\venv\xt
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
python -m src.vendors.xtquant.cli clean trade-cal
echo.

echo ----------------------------------------------------------------------------------
echo [STEP] Cleaning Identity
echo ----------------------------------------------------------------------------------
python -m src.vendors.xtquant.cli clean identity
echo.

echo ----------------------------------------------------------------------------------
echo [STEP] Cleaning 1-Day Bar (%START_DATE% - %END_DATE%)
echo ----------------------------------------------------------------------------------
python -m src.vendors.xtquant.cli clean 1day-bar --start %START_DATE% --end %END_DATE% --replace %replace%
echo.

echo ----------------------------------------------------------------------------------
echo [STEP] Cleaning 1-Min Bar (%START_DATE% - %END_DATE%)
echo ----------------------------------------------------------------------------------
python -m src.vendors.xtquant.cli clean 1min-bar --start %START_DATE% --end %END_DATE% --replace %replace%
echo.

echo ==================================================================================
echo  [DONE] XTQuant Clean Pipeline Completed.
echo  Time: %DATE% %TIME%
echo ==================================================================================
echo.

endlocal

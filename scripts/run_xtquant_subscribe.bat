@echo off
setlocal EnableDelayedExpansion

:: ==================================================================================
::  SCRIPT: XTQuant Subscribe Pipeline
::  DESC:   Subscribes to real-time quote data
:: ==================================================================================

cd /d "%~dp0.."
set "PROJECT_ROOT=%CD%"

echo.
echo ==================================================================================
echo  [START] XTQuant Subscribe Pipeline
echo  Time: %DATE% %TIME%
echo  Root: %PROJECT_ROOT%
echo ==================================================================================
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
::  Subscribe Phase
:: ----------------------------------------------------------------------------------

echo ----------------------------------------------------------------------------------
echo [STEP] Subscribing Real-time Quote
echo ----------------------------------------------------------------------------------
python -m src.vendors.xtquant.cli subscribe realtime-quote
echo.

echo ==================================================================================
echo  [DONE] XTQuant Subscribe Pipeline Completed.
echo  Time: %DATE% %TIME%
echo ==================================================================================
echo.

endlocal

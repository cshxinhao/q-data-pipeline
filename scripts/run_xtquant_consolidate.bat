@echo off
setlocal EnableDelayedExpansion

:: ==================================================================================
::  SCRIPT: XTQuant Consolidate Pipeline
::  DESC:   Consolidates realtime quote data
:: ==================================================================================

cd /d "%~dp0.."
set "PROJECT_ROOT=%CD%"

echo.
echo ==================================================================================
echo  [START] XTQuant Consolidate Pipeline
echo  Time: %DATE% %TIME%
echo  Root: %PROJECT_ROOT%
echo ==================================================================================
echo.

:: ----------------------------------------------------------------------------------
::  Configuration
:: ----------------------------------------------------------------------------------

:: Get Today's Date
for /f %%a in ('powershell -Command "Get-Date -Format yyyy-MM-dd"') do set TODAY=%%a
echo [INFO] Target Date: %TODAY%
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
::  Consolidate Phase
:: ----------------------------------------------------------------------------------

echo ----------------------------------------------------------------------------------
echo [STEP] Consolidating Realtime Quote (%TODAY%)
echo ----------------------------------------------------------------------------------
python -m src.vendors.xtquant.cli clean realtime-quote --date %TODAY%
echo.

echo ==================================================================================
echo  [DONE] XTQuant Consolidate Pipeline Completed.
echo  Time: %DATE% %TIME%
echo ==================================================================================
echo.

endlocal

@echo off
setlocal EnableDelayedExpansion

:: ==================================================================================
::  SCRIPT: Tushare Clean Dataset History
::  DESC:   Cleans Tushare dataset for a range of years (History)
:: ==================================================================================

cd /d "%~dp0.."
set "PROJECT_ROOT=%CD%"

echo.
echo ==================================================================================
echo  [START] Tushare Clean Dataset History
echo  Time: %DATE% %TIME%
echo  Root: %PROJECT_ROOT%
echo ==================================================================================
echo.

:: ----------------------------------------------------------------------------------
::  Configuration
:: ----------------------------------------------------------------------------------
set "START_YEAR=2012"
set "END_YEAR=2026"

echo [INFO] Year Range: %START_YEAR% to %END_YEAR%
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
::  Clean Phase (Loop)
:: ----------------------------------------------------------------------------------

FOR /L %%y IN (%START_YEAR%, 1, %END_YEAR%) DO (
    echo ----------------------------------------------------------------------------------
    echo [STEP] Cleaning Dataset Year: %%y
    echo ----------------------------------------------------------------------------------
    python -m src.vendors.tushare.cli clean dataset --year %%y --replace True
    echo.
)

echo ==================================================================================
echo  [DONE] Tushare Clean Dataset History Completed.
echo  Time: %DATE% %TIME%
echo ==================================================================================
echo.

pause
endlocal

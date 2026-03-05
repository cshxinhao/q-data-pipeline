@echo off
setlocal EnableDelayedExpansion

:: ==================================================================================
::  SCRIPT: Tushare Checker
::  DESC:   Runs data quality checks on Tushare data
:: ==================================================================================

cd /d "%~dp0.."
set "PROJECT_ROOT=%CD%"

echo.
echo ==================================================================================
echo  [START] Cross-Vendor Checker
echo  Time: %DATE% %TIME%
echo  Root: %PROJECT_ROOT%
echo ==================================================================================
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
::  Checks
:: ----------------------------------------------------------------------------------

echo ----------------------------------------------------------------------------------
echo [STEP] Checking Cross-Vendor Consistency
echo ----------------------------------------------------------------------------------
python -m src.checker.cli cross-check
echo.


echo ==================================================================================
echo  [DONE] Cross-Vendor Checker Completed.
echo  Time: %DATE% %TIME%
echo ==================================================================================
echo.

endlocal

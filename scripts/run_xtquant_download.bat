@echo off
setlocal EnableDelayedExpansion

:: ==================================================================================
::  SCRIPT: XTQuant Download Pipeline
::  DESC:   Downloads XTQuant data (Contracts, Sector, Index, Bar, Financial)
:: ==================================================================================

cd /d "%~dp0.."
set "PROJECT_ROOT=%CD%"

echo.
echo ==================================================================================
echo  [START] XTQuant Download Pipeline
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
::  Download Phase
:: ----------------------------------------------------------------------------------

echo ----------------------------------------------------------------------------------
echo [STEP] Downloading Contracts
echo ----------------------------------------------------------------------------------
python -m src.vendors.xtquant.cli download contracts
echo.

@REM echo ----------------------------------------------------------------------------------
@REM echo [STEP] Downloading Sector Data
@REM echo ----------------------------------------------------------------------------------
@REM python -m src.vendors.xtquant.cli download sector-data
@REM echo.

@REM echo ----------------------------------------------------------------------------------
@REM echo [STEP] Downloading Index Weight
@REM echo ----------------------------------------------------------------------------------
@REM python -m src.vendors.xtquant.cli download index-weight
@REM echo.

echo ----------------------------------------------------------------------------------
echo [STEP] Downloading 1-Day/1-Min Bar Prices
echo ----------------------------------------------------------------------------------
python -m src.vendors.xtquant.cli download bar
echo.

echo ----------------------------------------------------------------------------------
echo [STEP] Downloading Financial Data
echo ----------------------------------------------------------------------------------
python -m src.vendors.xtquant.cli download financial
echo.

echo ==================================================================================
echo  [DONE] XTQuant Download Pipeline Completed.
echo  Time: %DATE% %TIME%
echo ==================================================================================
echo.

endlocal

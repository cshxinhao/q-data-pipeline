@echo off
setlocal EnableDelayedExpansion

:: ==================================================================================
::  SCRIPT: Futu Daily Pipeline
::  DESC:   Downloads and cleans daily Futu data (Calendar, Mapper, Bar, Factors)
:: ==================================================================================

cd /d "%~dp0.."
set "PROJECT_ROOT=%CD%"

echo.
echo ==================================================================================
echo  [START] Futu Daily Pipeline
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
echo [INFO] Activating conda environment (futu)...
call conda activate %PROJECT_ROOT%\venv\futu
if %errorlevel% neq 0 (
    echo [ERROR] Failed to activate environment.
    exit /b %errorlevel%
)
echo.

:: ----------------------------------------------------------------------------------
::  Download Phase
:: ----------------------------------------------------------------------------------

echo ----------------------------------------------------------------------------------
echo [STEP] Downloading Trade Calendar (%START_DATE% - %END_DATE%)
echo ----------------------------------------------------------------------------------
python -m src.vendors.futu.cli download trade-cal --market HK --start %START_DATE% --end %END_DATE%
echo.

echo ----------------------------------------------------------------------------------
echo [STEP] Downloading HKEX Stock List
echo ----------------------------------------------------------------------------------
python -m src.vendors.futu.cli download hkex-stock-list --market HK
echo.

echo ----------------------------------------------------------------------------------
echo [STEP] Downloading Stock List
echo ----------------------------------------------------------------------------------
python -m src.vendors.futu.cli download stock-list --market HK
echo.

echo ----------------------------------------------------------------------------------
echo [STEP] Downloading Plate List
echo ----------------------------------------------------------------------------------
python -m src.vendors.futu.cli download plate-list --market HK
echo.

echo ----------------------------------------------------------------------------------
echo [STEP] Downloading Owner Plate
echo ----------------------------------------------------------------------------------
python -m src.vendors.futu.cli download owner-plate --market HK
echo.


:: ----------------------------------------------------------------------------------
::  Clean Phase
:: ----------------------------------------------------------------------------------

echo ----------------------------------------------------------------------------------
echo [STEP] Cleaning Trade Calendar
echo ----------------------------------------------------------------------------------
python -m src.vendors.futu.cli clean trade-cal --market HK
echo.

echo ----------------------------------------------------------------------------------
echo [STEP] Cleaning Identity
echo ----------------------------------------------------------------------------------
python -m src.vendors.futu.cli clean identity --market HK
echo.


echo ==================================================================================
echo  [DONE] Futu Daily Pipeline Completed.
echo  Time: %DATE% %TIME%
echo ==================================================================================
echo.

endlocal

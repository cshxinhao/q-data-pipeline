@echo off
setlocal EnableDelayedExpansion

:: ==================================================================================
::  SCRIPT: Tushare Download Pipeline
::  DESC:   Downloads Tushare data without cleaning
:: ==================================================================================

cd /d "%~dp0.."
set "PROJECT_ROOT=%CD%"

echo.
echo ==================================================================================
echo  [START] Tushare Download Pipeline
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

echo ==================================================================================
echo  [DONE] Tushare Download Pipeline Completed.
echo  Time: %DATE% %TIME%
echo ==================================================================================
echo.

endlocal

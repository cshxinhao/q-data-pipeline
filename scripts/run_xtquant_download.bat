@echo off
setlocal

:: ------------------------------------------------------------------------------
:: Prepare the directory and venv
:: Get the directory of the script and change to project root (one level up)
cd /d "%~dp0.."
set "PROJECT_ROOT=%CD%"
call conda activate %PROJECT_ROOT%\venv\xt
:: ------------------------------------------------------------------------------

echo Running XTQuant pipeline - download from %PROJECT_ROOT%

:: Download

@REM echo Step: Downloading contracts...
@REM python -m src.vendors.xtquant.cli download contracts

@REM echo Step: Downloading sector data...
@REM python -m src.vendors.xtquant.cli download sector-data

@REM echo Step: Downloading index-weight...
@REM python -m src.vendors.xtquant.cli download index-weight

@REM echo Step: Downloading 1-day/1-min bar prices...
@REM python -m src.vendors.xtquant.cli download bar

echo Step: Downloading financial data...
python -m src.vendors.xtquant.cli download financial


echo XTQuant pipeline - download completed.

endlocal
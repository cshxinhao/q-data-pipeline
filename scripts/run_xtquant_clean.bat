@echo off
setlocal

:: Preparation
cd /d "%~dp0.."
set "PROJECT_ROOT=%CD%"
call conda activate %PROJECT_ROOT%\venv\xt

:: Set params
@REM set "START_DATE=20120101"
set "START_DATE=20260227"
set "END_DATE=20260228"
set "replace=True"


echo Running XTQuant pipeline - clean from %PROJECT_ROOT%

:: Clean

echo Step: Cleaning trade calendar...
python -m src.vendors.xtquant.cli clean trade-cal

echo Step: Cleaning identity...
python -m src.vendors.xtquant.cli clean identity

echo Step: Cleaning 1day bar...
python -m src.vendors.xtquant.cli clean 1day-bar --start %START_DATE% --end %END_DATE% --replace %replace%


echo XTQuant pipeline - clean completed.

endlocal
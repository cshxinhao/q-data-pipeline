@echo off
setlocal

:: Get the directory of the script and change to project root (one level up)
cd /d "%~dp0.."
set "PROJECT_ROOT=%CD%"

echo Running checker on Tushare data from %PROJECT_ROOT%

:: Activate the env
call conda activate %PROJECT_ROOT%\venv\tushare


echo Step: Checking nulls...
python -m src.checker.cli null --market China --vendor tushare

echo Step: Checking duplicate...
python -m src.checker.cli duplicate --market China --vendor tushare

echo Step: Checking volume...
python -m src.checker.cli volume --market China --vendor tushare

echo Step: Checking returns outlier...
python -m src.checker.cli returns-outlier --market China --vendor tushare

echo Step: Checking logic consistency...
python -m src.checker.cli logic-consistency --market China --vendor tushare


echo Checker completed.

endlocal
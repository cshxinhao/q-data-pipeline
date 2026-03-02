@echo off
setlocal enabledelayedexpansion

:: call _run_tushare_download_first.bat
call _run_tushare_by_category.bat

echo Tushare pipeline completed.

endlocal

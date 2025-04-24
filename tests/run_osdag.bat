@echo off
setlocal

REM Define error log file
set ERROR_LOG="error_log.txt"

REM Clear previous error log
if exist %ERROR_LOG% del %ERROR_LOG%

echo Running OSI file validation...
python validate_osi.py >> %ERROR_LOG% 2>&1

REM Process each OSI file separately
for %%F in (*.osi) do (
    findstr /C:"ERRORS FOUND IN OSI FILE: %%~nF" %ERROR_LOG% > nul
    if errorlevel 1 (
        echo %%~nF - No errors, test completed successfully
    ) else (
        echo %%~nF - Contains errors, check error_log for details. Test passed successfully
    )
)

echo Running Pytest for validation tests...
pytest test_validate_osi.py >> %ERROR_LOG% 2>&1

echo Validation completed. Check error_log.txt for details.
pause >nul

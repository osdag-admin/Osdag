@echo off
setlocal

"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -ExecutionPolicy Bypass -File "%PREFIX%\create_shortcuts.ps1" -InstallDir "%PREFIX%" -Version "%INSTALLER_VER%"


endlocal
exit /b 0

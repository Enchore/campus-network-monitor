@echo off
echo Stopping monitor...
taskkill /F /IM python.exe 2>nul
del /F "%~dp0.monitor.lock" 2>nul
echo Monitor stopped.
pause

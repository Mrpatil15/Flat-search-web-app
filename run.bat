@echo off
title Real Estate Aggregator
echo ==============================================
echo   Starting Real Estate Aggregator API...
echo ==============================================
echo.

:: Start python server in a new console window so it runs in the background
start "Real Estate Aggregator Server" cmd /k "cd /d %~dp0 && python app.py"

echo Waiting 3 seconds for the server to initialize...
timeout /t 3 /nobreak >nul

echo.
echo ==============================================
echo   Opening Search Dashboard in your Browser...
echo ==============================================
start "" "%~dp0index.html"

echo.
echo Done! Keep the server command window open while searching.
echo You can close this window now.
timeout /t 5 >nul
exit

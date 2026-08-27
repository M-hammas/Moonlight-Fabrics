@echo off
cd /d "%~dp0"
echo Starting Sidra Fabrics Ecommerce from:
echo %CD%
echo.
call npm install
echo.
call npm run dev
pause

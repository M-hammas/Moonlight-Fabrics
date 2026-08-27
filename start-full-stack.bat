@echo off
cd /d "%~dp0"
where docker >nul 2>nul
if errorlevel 1 (
  echo Docker Desktop was not found on PATH.
  echo Install/start Docker Desktop, then run this file again.
  pause
  exit /b 1
)
echo Starting Sidra Fabrics full stack...
docker compose up --build
pause

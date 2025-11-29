@echo off
chcp 65001 >nul
set /p TOR_PATH=<"%~dp0tor_path.txt"
"%TOR_PATH%" ^
  --SOCKSPort 9050 ^
  --ControlPort 9051 ^
  --CookieAuthentication 1 ^
  --MaxCircuitDirtiness 10 ^
  --DataDirectory "%~dp0tor_data"
pause
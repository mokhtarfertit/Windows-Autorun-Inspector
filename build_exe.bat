@echo off
cd /d "%~dp0"
echo Building CyberPersist executable...

if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

python -m PyInstaller --onedir --name cyberpersist --console --icon assets\cyberpersist.ico app\main.py

if errorlevel 1 (
    echo ERROR: PyInstaller build failed.
    pause
    exit /b 1
)

if not exist dist\cyberpersist\cyberpersist.exe (
    echo ERROR: cyberpersist.exe was not created.
    pause
    exit /b 1
)

echo.
echo Build finished.
echo EXE location: dist\cyberpersist\cyberpersist.exe
pause
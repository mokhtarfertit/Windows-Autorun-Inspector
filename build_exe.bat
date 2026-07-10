@echo off
echo Building CyberPersist installer...

set "ISCC_PATH=C:\Program Files (x86)\Inno Setup 7\ISCC.exe"

if not exist "%ISCC_PATH%" (
    set "ISCC_PATH=C:\Program Files\Inno Setup 7\ISCC.exe"
)

if not exist "%ISCC_PATH%" (
    set "ISCC_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
)

if not exist "%ISCC_PATH%" (
    set "ISCC_PATH=C:\Program Files\Inno Setup 6\ISCC.exe"
)

if not exist "%ISCC_PATH%" (
    echo ERROR: Inno Setup Compiler not found.
    echo Check where ISCC.exe is installed and update ISCC_PATH.
    pause
    exit /b 1
)

if not exist dist\cyberpersist\cyberpersist.exe (
    echo ERROR: cyberpersist.exe not found.
    echo Run build_exe.bat first.
    pause
    exit /b 1
)

if not exist dist-installer mkdir dist-installer

"%ISCC_PATH%" installer\cyberpersist.iss

if errorlevel 1 (
    echo ERROR: Installer build failed.
    pause
    exit /b 1
)

echo.
echo Installer build finished.
echo Installer location: dist-installer\CyberPersist-Setup.exe
pause
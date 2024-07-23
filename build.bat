@echo off
setlocal

set SCRIPT_NAME=menu.py
set ICON_NAME=banana.ico
set EXE_NAME=BananaDropFarm
set SPEC_FILE=%EXE_NAME%.spec
set DIST_DIR=dist
set BUILD_DIR=build
set EXE_PATH=%DIST_DIR%\%EXE_NAME%.exe

call setup.bat

echo This script will turn %EXE_NAME% into an executable.
echo The --noconsole option hides the console window when you run the executable.
echo If you set debug to true in %SCRIPT_NAME%, you will not be able to see the output if you use --noconsole.
echo Do you want to use the --noconsole option? (y/n)
set /p noconsole_choice=

if /I "%noconsole_choice%" NEQ "y" if /I "%noconsole_choice%" NEQ "n" (
    echo Invalid choice. Please run the script again and enter 'y' or 'n'.
    pause
    exit /b 1
)

if /I "%noconsole_choice%" == "y" (
    pyinstaller --onefile --noconsole %SCRIPT_NAME% -i "%ICON_NAME%" -n "%EXE_NAME%"
) else (
    pyinstaller --onefile %SCRIPT_NAME% -i "%ICON_NAME%" -n "%EXE_NAME%"
)

if errorlevel 1 (
    echo PyInstaller failed to build the executable.
    pause
    exit /b 1
) else (
    echo PyInstaller build succeeded.
)

if exist "%EXE_PATH%" (
    move "%EXE_PATH%" .
    if errorlevel 1 (
        echo Failed to move the executable.
        pause
        exit /b 1
    ) else (
        echo Successfully moved the executable to the current directory.
    )
) else (
    echo The executable was not found in the %DIST_DIR% folder.
    pause
    exit /b 1
)

echo Deleting the %DIST_DIR% folder...
rmdir /s /q %DIST_DIR%

echo Deleting the %BUILD_DIR% folder...
rmdir /s /q %BUILD_DIR%

echo Deleting the %SPEC_FILE% file...
del /q %SPEC_FILE%

echo Cleanup completed.

pause
endlocal
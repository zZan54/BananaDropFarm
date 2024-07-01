@echo off
call setup.bat

echo This script will turn BananaDropFarm into an executable.
echo The --noconsole option hides the console window when you run the executable.
echo If you set debug to true in menu.py, you will not be able to see the output if you use --noconsole.
echo Do you want to use the --noconsole option? (y/n)
set /p noconsole_choice=

if /I "%noconsole_choice%" == "y" (
    pyinstaller --onefile --noconsole menu.py -i "banana.ico" -n "BananaDropFarm"
) else (
    pyinstaller --onefile menu.py -i "banana.ico" -n "BananaDropFarm"
)

if errorlevel 1 (
    echo PyInstaller failed to build the executable.
    pause
    exit /b 1
) else (
    echo PyInstaller build succeeded.
)

if exist "dist\BananaDropFarm.exe" (
    move "dist\BananaDropFarm.exe" .
    if errorlevel 1 (
        echo Failed to move the executable.
        pause
        exit /b 1
    ) else (
        echo Successfully moved the executable to the current directory.
    )
) else (
    echo The executable was not found in the dist folder.
    pause
    exit /b 1
)

pause

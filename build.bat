@echo off
call setup.bat

pyinstaller --onefile --noconsole menu.py -i "banana.ico" -n "BananaDropFarm"
pause
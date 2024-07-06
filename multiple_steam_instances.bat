REM This script is an example of how to run multiple instances of Steam on the same computer.
REM Please use multiplesteaminstances.py to generate this script instead of running it directly.

@echo off
start "Steam1" "C:/Program Files (x86)/Steam/steam.exe" -master_ipc_name_override steam1
start "Steam2" "C:/Program Files (x86)/Steam/steam.exe" -master_ipc_name_override steam2
pause
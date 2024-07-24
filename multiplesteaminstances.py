import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox

def search_steam():
    default_path = r"C:\Program Files (x86)\Steam\steam.exe"
    if os.path.isfile(default_path):
        print(f"steam.exe found in the default directory: {default_path}")
        return default_path
    return None

def select_steam():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select steam.exe",
        filetypes=(("Executable files", "*.exe"), ("All files", "*.*"))
    )
    if not file_path:
        messagebox.showerror("Error", "No file selected. Exiting.")
        sys.exit()
    if not file_path.endswith("steam.exe"):
        messagebox.showerror("Error", "Selected file is not steam.exe. Exiting.")
        sys.exit()
    return file_path

def steam_instances_number():
    while True:
        try:
            instances = int(input("Enter the number of Steam instances you want to run (1-10): "))
            if 1 <= instances <= 10:
                return instances
            else:
                print("Please enter a number between 1 and 10.")
        except Exception:
            print("Invalid input. Please enter a number between 1 and 10.")

def steam_instances_script(steampath, instances):
    script_content = "@echo off\n"
    for i in range(1, instances + 1):
        script_content += f'start "Steam{i}" "{steampath}" -master_ipc_name_override steam{i}\n'
    script_content += "pause\n"

    script_path = os.path.join(os.getcwd(), "multiple_steam_instances.bat")
    with open(script_path, "w") as f:
        f.write(script_content)
    print(f"Script created at {script_path}.")
    print("Run the script to start multiple Steam instances.")

def main():
    print("Note: Make sure you're logged out of Steam before continuing.")

    try:
        continue_input = input("Press Enter to continue or Ctrl+C to exit.")
    except KeyboardInterrupt:
        sys.exit()
    
    steampath = search_steam()
    if not steampath:
        print("steam.exe not found in the default directory. Please select the steam.exe file.")
        steampath = select_steam()
    
    instances = steam_instances_number()
    steam_instances_script(steampath, instances)

if __name__ == "__main__":
    main()
from colorsys import hsv_to_rgb
from pymem.process import *
import time
import pymem
import random
import threading
import customtkinter
import webbrowser

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

pm = pymem.Pymem("Banana.exe")
gameModule = module_from_name(pm.process_handle, "GameAssembly.dll").lpBaseOfDll

def GetPtrAddr(base, offsets):
    addr = pm.read_longlong(base)
    for offset in offsets:
        if offset != offsets[-1]:
            addr = pm.read_longlong(addr + offset)
    return addr + offsets[-1]

app = customtkinter.CTk()
app.title("Banana Drop Farm")
app.geometry("550x350")
app.resizable(False, False)

try:
    app.iconbitmap("banana.ico")
except Exception:
    pass

def changescore():
    score = int(scorevalue.get())
    try:
        pm.write_int(GetPtrAddr(gameModule + 0x00EA7648, [0x4A8, 0x78, 0x48, 0xB8, 0x88, 0x60, 0x28]), score)
    except Exception:
        print("An error occurred while trying to set the score.")
        break

def botidlecheckbypass():
    def update_score():
        try:
            while botidlecheckbypass_var.get():
                current_score = pm.read_int(GetPtrAddr(gameModule + 0x00EA7648, [0x4A8, 0x78, 0x48, 0xB8, 0x88, 0x60, 0x28]))
                new_score = current_score + random.randint(1, 25)
                pm.write_int(GetPtrAddr(gameModule + 0x00EA7648, [0x4A8, 0x78, 0x48, 0xB8, 0x88, 0x60, 0x28]), new_score)
                time.sleep(2)
        except Exception:
            pass

    thread = threading.Thread(target=update_score)
    thread.daemon = True
    thread.start()

options = customtkinter.CTkTabview(master=app, width=520, height=300)
options.pack(anchor=customtkinter.CENTER)

options.add("Cheat")
options.add("Info")
options.set("Cheat")

score = customtkinter.CTkFrame(master=options.tab("Cheat"))
score.pack(side="top", padx=20, pady=8)

scorechanger = customtkinter.CTkLabel(master=score, text="Score Changer:", fg_color="transparent")
scorechanger.pack(side="left", padx=5)

scorevalue = customtkinter.CTkEntry(master=score, placeholder_text="Value")
scorevalue.pack(side="left", padx=5)

setscore = customtkinter.CTkButton(master=score, text="Set Score", command=changescore)
setscore.pack(side="left", padx=5)

botidlecheckbypass_var = customtkinter.BooleanVar(value=False)
botidlecheckbypass = customtkinter.CTkCheckBox(master=options.tab("Cheat"), text="Bot Idle Check Bypass", command=botidlecheckbypass, variable=botidlecheckbypass_var)
botidlecheckbypass.pack(padx=20, pady=8, anchor=customtkinter.CENTER)

scorechangerinfo = customtkinter.CTkLabel(master=options.tab("Info"), text="Score Changer - changes score", fg_color="transparent", text_color="white")
scorechangerinfo.pack(padx=20, pady=8, anchor=customtkinter.CENTER)

botidlecheckbypassinfo = customtkinter.CTkLabel(master=options.tab("Info"), text="Bot Idle Check Bypass - bypasses the bot idle check by adding a random \nvalue from 1 to 25 to the current score every 2 seconds", fg_color="transparent", text_color="white")
botidlecheckbypassinfo.pack(padx=20, pady=8, anchor=customtkinter.CENTER)

note = customtkinter.CTkLabel(master=options.tab("Info"), text="Note: You need to click for the score to update", fg_color="transparent", text_color="white")
note.pack(padx=20, pady=8, anchor=customtkinter.CENTER)

githublink = customtkinter.CTkLabel(app, text="github.com/zZan54", fg_color="transparent", text_color="white")
githublink.place(x=220, y=310)
githublink.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/zZan54"))

animation_running = True

def githublinkanimation():
    colors = [f"#{''.join(f'{int(c * 255):02x}' for c in hsv_to_rgb(i / 360, 1, 1))}" for i in range(360)]
    i = 0
    direction = 1
    while animation_running:
        if i >= 350:
            direction = -1
        elif i <= 50:
            direction = 1
        i += direction
        githublink.place(x=10 + i, y=310)
        githublink.configure(text_color=colors[i])
        time.sleep(0.01)

def on_close():
    global animation_running
    animation_running = False
    app.destroy()

app.protocol("WM_DELETE_WINDOW", on_close)

githublinkanimationthread = threading.Thread(target=githublinkanimation)
githublinkanimationthread.daemon = True
githublinkanimationthread.start()

app.mainloop()

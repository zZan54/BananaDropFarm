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

try:
    game = pymem.Pymem("Banana.exe")
    gameModule = module_from_name(game.process_handle, "GameAssembly.dll").lpBaseOfDll
except Exception:
    print("Error: Could not find the game process. Make sure the game is running.")
    exit()

def GetPtrAddr(base, offsets):
    addr = game.read_longlong(base)
    for offset in offsets:
        if offset != offsets[-1]:
            addr = game.read_longlong(addr + offset)
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
    new_score = int(scorevalue.get())
    try:
        game.write_int(GetPtrAddr(gameModule + 0x00EA7648, [0x4A8, 0x78, 0x48, 0xB8, 0x88, 0x60, 0x28]), new_score)
    except Exception:
        print("An error occurred while trying to set the score.")
        exit()

def botidlecheckbypass():
    if botidlecheckbypassdelay_var.get() != None:
        botidlecheckbypassdelay = float(botidlecheckbypassdelay_var.get())
    else:
        botidlecheckbypassdelay = 2.0

    if botidlecheckbypassmethod_var.get() == "Random increment":
        def update_score():
            try:
                while botidlecheckbypass_var.get():
                    current_score = game.read_int(GetPtrAddr(gameModule + 0x00EA7648, [0x4A8, 0x78, 0x48, 0xB8, 0x88, 0x60, 0x28]))
                    new_score = current_score + random.randint(1, 25)
                    game.write_int(GetPtrAddr(gameModule + 0x00EA7648, [0x4A8, 0x78, 0x48, 0xB8, 0x88, 0x60, 0x28]), new_score)
                    time.sleep(botidlecheckbypassdelay)
            except Exception:
                print("An error occurred while trying to bypass the bot idle check.")
                pass

    elif botidlecheckbypassmethod_var.get() == "Random value":
        def update_score():
            try:
                while botidlecheckbypass_var.get():
                    new_score = random.randint(1, 1000000)
                    game.write_int(GetPtrAddr(gameModule + 0x00EA7648, [0x4A8, 0x78, 0x48, 0xB8, 0x88, 0x60, 0x28]), new_score)
                    time.sleep(botidlecheckbypassdelay)
            except Exception:
                print("An error occurred while trying to bypass the bot idle check.")
                pass

    elif botidlecheckbypassmethod_var.get() == "Increment":
        def update_score():
            try:
                while botidlecheckbypass_var.get():
                    current_score = game.read_int(GetPtrAddr(gameModule + 0x00EA7648, [0x4A8, 0x78, 0x48, 0xB8, 0x88, 0x60, 0x28]))
                    new_score = current_score + 1
                    game.write_int(GetPtrAddr(gameModule + 0x00EA7648, [0x4A8, 0x78, 0x48, 0xB8, 0x88, 0x60, 0x28]), new_score)
                    time.sleep(botidlecheckbypassdelay)
            except Exception:
                print("An error occurred while trying to bypass the bot idle check.")
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

botidlecheckbypassall = customtkinter.CTkFrame(master=options.tab("Cheat"))
botidlecheckbypassall.pack(side="top", padx=20, pady=8)

botidlecheckbypass_var = customtkinter.BooleanVar(value=False)
botidlecheckbypass = customtkinter.CTkCheckBox(master=botidlecheckbypassall, text="Bot Idle Check Bypass", command=botidlecheckbypass, variable=botidlecheckbypass_var)
botidlecheckbypass.pack(side="left", padx=5)

botidlecheckbypassmethod_var = customtkinter.StringVar(value="Random increment")
botidlecheckbypassmethod = customtkinter.CTkComboBox(master=botidlecheckbypassall, values=["Random increment", "Random value", "Increment"], variable=botidlecheckbypassmethod_var, width=150)
botidlecheckbypassmethod.pack(side="left", padx=5)
botidlecheckbypassmethod_var.set("Random increment")

botidlecheckbypassdelay_var = customtkinter.StringVar(value='2')
botidlecheckbypassdelay = customtkinter.CTkComboBox(master=botidlecheckbypassall, values=['0.5', '1', '2', '5', '10', '15', '30', '45', '60', '120', '180', '300'], variable=botidlecheckbypassdelay_var, width=60)
botidlecheckbypassdelay.pack(side="left", padx=5)
botidlecheckbypassdelay_var.set('2')

scorechangerinfo = customtkinter.CTkLabel(master=options.tab("Info"), text="Score Changer - changes score", fg_color="transparent", text_color="white")
scorechangerinfo.pack(padx=20, pady=8, anchor=customtkinter.CENTER)

botidlecheckbypassinfo = customtkinter.CTkLabel(master=options.tab("Info"), text="Bot Idle Check Bypass - bypasses the bot idle check depending on \nwhat method you chose", fg_color="transparent", text_color="white")
botidlecheckbypassinfo.pack(padx=20, pady=8, anchor=customtkinter.CENTER)

botidlecheckbypassmethodsinfo = customtkinter.CTkLabel(master=options.tab("Info"), text="Bypass methods: \nRandom Increment - adds a random number from 1 to 25 to the current score \nRandom value - changes the current score to a random value \nIncrement - adds 1 to the current score", fg_color="transparent", text_color="white")
botidlecheckbypassmethodsinfo.pack(padx=20, pady=8, anchor=customtkinter.CENTER)

notes = customtkinter.CTkLabel(master=options.tab("Info"), text=f"Notes: \nThe chosen method is activated every few seconds, depending on the delay you choose. \nDefault delay is 2 seconds. You need to click for the score to update.", fg_color="transparent", text_color="white")
notes.pack(padx=20, pady=8, anchor=customtkinter.CENTER)

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

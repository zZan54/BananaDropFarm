import time
import pymem
import ctypes
import random
import threading
import customtkinter
import webbrowser

from pystyle import Colorate, Colors, Center
from colorsys import hsv_to_rgb
from pymem.process import *

debug = True

class DebugLog:
    def __init__(self, debug=debug):
        self.debug = debug

    def _log(self, message):
        if self.debug:
            print(message)
        else:
            pass
    
    def info(self, message):
        self._log(f"{Colors.green}[+] {Colors.reset}{message}")
    
    def error(self, message):
        self._log(f"{Colors.red}[-] {Colors.reset}{message}")
    
    def warning(self, message):
        self._log(f"{Colors.cyan}[!] {Colors.reset}{message}")

bananadropfarmlog = DebugLog()

ctypes.windll.kernel32.SetConsoleTitleW("Banana Drop Farm v1.3 | github.com/zZan54")

bananadropfarm = Center.XCenter("\nBanana Drop Farm v1.3\n")
print(Colorate.Horizontal(Colors.yellow_to_red, bananadropfarm, 1))

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

try:
    game = pymem.Pymem("Banana.exe")
    gameModule = module_from_name(game.process_handle, "UnityPlayer.dll").lpBaseOfDll
    bananadropfarmlog.info("Successfully found the game process.")
except Exception:
    bananadropfarmlog.error("An error occurred while trying to find the game process. Exiting...")
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
    bananadropfarmlog.info("Successfully set the app icon.")
except Exception:
    bananadropfarmlog.warning("An error occurred while trying to set the app icon. Using the default icon.")
    pass

score_addr = gameModule + 0x01CFD6C8
score_offsets = [0x20, 0xA68, 0x18, 0xA0, 0x90, 0x28, 0x30]

def changescore():
    new_score = int(scorevalue.get())
    try:
        game.write_int(GetPtrAddr(score_addr, score_offsets), new_score)
        bananadropfarmlog.info(f"Successfully set the score to {new_score}.")
    except Exception:
        bananadropfarmlog.error(f"An error occurred while trying to set the score to {new_score}.")
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
                    current_score = game.read_int(GetPtrAddr(score_addr, score_offsets))
                    new_score = current_score + random.randint(1, 25)
                    game.write_int(GetPtrAddr(score_addr, score_offsets), new_score)
                    time.sleep(botidlecheckbypassdelay)
            except Exception:
                bananadropfarmlog.error("An error occurred while trying to bypass the bot idle check.")
                pass

    elif botidlecheckbypassmethod_var.get() == "Random value":
        def update_score():
            try:
                while botidlecheckbypass_var.get():
                    new_score = random.randint(1, 1000000)
                    game.write_int(GetPtrAddr(score_addr, score_offsets), new_score)
                    time.sleep(botidlecheckbypassdelay)
            except Exception:
                bananadropfarmlog.error("An error occurred while trying to bypass the bot idle check.")
                pass

    elif botidlecheckbypassmethod_var.get() == "Increment":
        def update_score():
            try:
                while botidlecheckbypass_var.get():
                    current_score = game.read_int(GetPtrAddr(score_addr, score_offsets))
                    new_score = current_score + 1
                    game.write_int(GetPtrAddr(score_addr, score_offsets), new_score)
                    time.sleep(botidlecheckbypassdelay)
            except Exception:
                bananadropfarmlog.error("An error occurred while trying to bypass the bot idle check.")
                pass

    if botidlecheckbypass_var.get():
        bananadropfarmlog.info(f"Bot idle check bypass has been activated | Method: {botidlecheckbypassmethod_var.get()} | Delay: {botidlecheckbypassdelay} seconds")
    else:
        bananadropfarmlog.info("Bot idle check bypass has been deactivated")

    thread = threading.Thread(target=update_score)
    thread.daemon = True
    thread.start()

def spoofcps():
    if spoofcpsdelay_var.get() != None:
        spoofcpsdelay = float(spoofcpsdelay_var.get())
    else:
       spoofcpsdelay = 0.5

    if spoofcpsmethod_var.get() == "Random":
        def update_cps():
            try:
                while spoofcps_var.get():
                    new_cps = random.randint(1, 1000000)
                    game.write_int(GetPtrAddr(score_addr, score_offsets) + 0x10, new_cps)
                    time.sleep(spoofcpsdelay)
            except Exception:
                bananadropfarmlog.error("An error occurred while trying to spoof cps.")
                pass

    elif spoofcpsmethod_var.get() == "Random normal":
        def update_cps():
            try:
                while spoofcps_var.get():
                    new_cps = random.randint(1, 20)
                    game.write_int(GetPtrAddr(score_addr, score_offsets) + 0x10, new_cps)
                    time.sleep(spoofcpsdelay)
            except Exception:
                bananadropfarmlog.error("An error occurred while trying to spoof cps.")
                pass

    elif spoofcpsmethod_var.get() == "Static":
        def update_cps():
            try:
                while spoofcps_var.get():
                    game.write_int(GetPtrAddr(score_addr, score_offsets) + 0x10, 15)
                    time.sleep(spoofcpsdelay)
            except Exception:
                bananadropfarmlog.error("An error occurred while trying to spoof cps.")
                pass

    if spoofcps_var.get():
        bananadropfarmlog.info(f"Cps spoof has been activated | Method: {spoofcpsmethod_var.get()} | Delay: {spoofcpsdelay} seconds")
    else:
        bananadropfarmlog.info("Cps spoof has been deactivated")

    thread = threading.Thread(target=update_cps)
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

spoofcpsall = customtkinter.CTkFrame(master=options.tab("Cheat"))
spoofcpsall.pack(side="top", padx=20, pady=8)

spoofcps_var = customtkinter.BooleanVar(value=False)
spoofcps = customtkinter.CTkCheckBox(master=spoofcpsall, text="Spoof Cps", command=spoofcps, variable=spoofcps_var)
spoofcps.pack(side="left", padx=5)

spoofcpsmethod_var = customtkinter.StringVar(value="Random normal")
spoofcpsmethod = customtkinter.CTkComboBox(master=spoofcpsall, values=["Random", "Random normal", "Static"], variable=spoofcpsmethod_var, width=150)
spoofcpsmethod.pack(side="left", padx=5)
spoofcpsmethod_var.set("Random normal")

spoofcpsdelay_var = customtkinter.StringVar(value='0.5')
spoofcpsdelay = customtkinter.CTkComboBox(master=spoofcpsall, values=['0.5', '1', '2', '5', '10', '15', '30', '45', '60', '120', '180', '300'], variable=spoofcpsdelay_var, width=60)
spoofcpsdelay.pack(side="left", padx=5)
spoofcpsdelay_var.set('0.5')

info = """Score Changer - changes score

Bot Idle Check Bypass - bypasses the bot idle check depending on what 
method you chose

Spoof Cps - spoofes the cps value depending on what method you chose

Bypass methods: 
 - Random Increment - adds a random number from 1 to 25 to 
   the current score 
 - Random value - changes the current score to a random value 
 - Increment - adds 1 to the current score

Spoof methods:
 - Random - sets a random cps value
 - Random normal - sets a random cps value from 1 to 20
 - Static - sets a static cps value of 15

Notes: 
 - The chosen method is activated every few seconds, 
   depending on the delay you choose. 
 - Default delay is 2 seconds.
 - You need to click for the score to update.
"""
infobox = customtkinter.CTkTextbox(master=options.tab("Info"), height=230, width=460)
infobox.insert("0.0", info)
infobox.configure(state="disabled")
infobox.pack(padx=20, pady=8, anchor=customtkinter.CENTER)

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

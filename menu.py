import time
import pymem
import yaml
import psutil
import ctypes
import random
import threading
import customtkinter
import webbrowser
import os

from pystyle import Colorate, Colors, Center
from colorsys import hsv_to_rgb
from pymem.process import module_from_name
import datetime

debug = True
savelogs = True

class DebugLog:
    def __init__(self, debug=debug):
        self.debug = debug
        self.log_file = "logs/logs.txt"

    def _log(self, message):
        if self.debug:
            print(message)
        else:
            pass
    
    def _savetofile(self, message, type):
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not os.path.exists("logs"):
            os.makedirs("logs")

        if type == "info":
            try:
                with open(self.log_file, "a") as file:
                    file.write(f"[{time}][+] {message}\n")
            except Exception:
                pass

        elif type == "error":
            try:
                with open(self.log_file, "a") as file:
                    file.write(f"[{time}][-] {message}\n")
            except Exception:
                pass

        elif type == "warning":
            try:
                with open(self.log_file, "a") as file:
                    file.write(f"[{time}][!] {message}\n")
            except Exception:
                pass
    
    def info(self, message):
        self._log(f"{Colors.green}[+] {Colors.reset}{message}")
        if savelogs == True:
            self._savetofile(message, "info")
        else:
            pass
    
    def error(self, message):
        self._log(f"{Colors.red}[-] {Colors.reset}{message}")
        if savelogs == True:
            self._savetofile(message, "error")
        else:
            pass
    
    def warning(self, message):
        self._log(f"{Colors.cyan}[!] {Colors.reset}{message}")
        if savelogs == True:
            self._savetofile(message, "warning")
        else:
            pass

bananadropfarmlog = DebugLog()

ctypes.windll.kernel32.SetConsoleTitleW("Banana Drop Farm v1.5 | github.com/zZan54")

bananadropfarm = Center.XCenter("\nBanana Drop Farm v1.5\n")
print(Colorate.Horizontal(Colors.yellow_to_red, bananadropfarm, 1))

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

def get_banana_processes():
    processes = []
    try:
        for proc in psutil.process_iter(attrs=['pid', 'name']):
            if proc.info['name'] == 'Banana.exe':
                processes.append(proc.info['pid'])
        return processes
    except Exception:
        bananadropfarmlog.error("An error occurred while trying to get the Banana processes.")
        exit()

try:
    banana_processes = get_banana_processes()
    if len(banana_processes) == 0:
        bananadropfarmlog.error("Banana process not found. Exiting...")
        exit()
    else:
        game_instances = []
        for banana_process in banana_processes:
            try:
                game = pymem.Pymem(banana_process)
                gameModule = module_from_name(game.process_handle, "UnityPlayer.dll").lpBaseOfDll
                game_instances.append((game, gameModule))
                bananadropfarmlog.info(f"Successfully found the game process with PID {banana_process}.")
            except Exception:
                bananadropfarmlog.error(f"An error occurred while trying to find the game process with PID {banana_process}.")
                continue
except Exception:
    bananadropfarmlog.error(f"An error occurred while trying to find the game process. Exiting...")
    exit()

def get_configs():
    configs = []
    try:
        for file in os.listdir("configs"):
            if file.endswith(".yaml"):
                configs.append(file)
    except Exception:
        bananadropfarmlog.warning("An error occurred while trying to get the configs. Using no configs.")
        pass
    return configs

def load_config():
    config_name = loadconfigname_var.get()
    with open(f'configs/{config_name}', 'r') as config_file:
        config = yaml.safe_load(config_file)

    botidlecheckbypassmethod_var.set(config['botidlecheckbypass']['method'])
    botidlecheckbypassdelay_var.set(config['botidlecheckbypass']['delay'])

    botidlecheckbypass_var.set(config['botidlecheckbypass']['enabled'])
    if botidlecheckbypass_var.get():
        botidlecheckbypass1()

    spoofcpsmethod_var.set(config['spoofcps']['method'])
    spoofcpsdelay_var.set(config['spoofcps']['delay'])

    spoofcps_var.set(config['spoofcps']['enabled'])
    if spoofcps_var.get():
        spoofcps1()

    idletimerreset_var.set(config['idletimerreset']['enabled'])
    if idletimerreset_var.get():
        idletimerreset1()

def save_config():
    config = {
        "botidlecheckbypass": {
            "enabled": botidlecheckbypass_var.get(),
            "method": botidlecheckbypassmethod_var.get(),
            "delay": botidlecheckbypassdelay_var.get()
        },
        "spoofcps": {
            "enabled": spoofcps_var.get(),
            "method": spoofcpsmethod_var.get(),
            "delay": spoofcpsdelay_var.get()
        },
        "idletimerreset": {
            "enabled": idletimerreset_var.get()
        }
    }

    config_name = saveconfigname.get()
    config_name = config_name.replace('.yaml', '')

    if config_name == "" or config_name == None:
        bananadropfarmlog.error("Please enter a config name.")
        return

    try:
        with open(f"configs/{config_name}.yaml", "w") as config_file:
            yaml.dump(config, config_file)
        bananadropfarmlog.info(f"Successfully saved the config as {config_name}.yaml")
    except Exception:
        bananadropfarmlog.error("An error occurred while trying to save the config.")
        pass

def GetPtrAddr(game, base, offsets):
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

score_addr = 0x1BFDFC0
score_offsets = [0x100, 0x1C0, 0x80, 0xE8, 0x78, 0x60, 0xA0]
cps_offset = 0x10
idletimer_offset = 0xC

def changescore():
    try:
        new_score = int(scorevalue.get())
    except Exception:
        bananadropfarmlog.error("Please enter a valid score value.")
        return
    for game, gameModule in game_instances:
        try:
            game.write_int(GetPtrAddr(game, gameModule + score_addr, score_offsets), new_score)
            bananadropfarmlog.info(f"Successfully set the score to {new_score}.")
        except Exception:
            bananadropfarmlog.error(f"An error occurred while trying to set the score to {new_score}.")
            continue

def resetscore1():
    for game, gameModule in game_instances:
        try:
            game.write_int(GetPtrAddr(game, gameModule + score_addr, score_offsets), 0)
            bananadropfarmlog.info("Successfully reset the score.")
        except Exception:
            bananadropfarmlog.error("An error occurred while trying to reset the score.")
            continue

def botidlecheckbypass1():
    if botidlecheckbypassdelay_var.get() != None:
        botidlecheckbypassdelay = float(botidlecheckbypassdelay_var.get())
    else:
        botidlecheckbypassdelay = 2.0

    if botidlecheckbypassmethod_var.get() == "Random increment":
        def update_score():
            while botidlecheckbypass_var.get():
                for game, gameModule in game_instances:
                    try:
                        current_score = game.read_int(GetPtrAddr(game, gameModule + score_addr, score_offsets))
                        new_score = current_score + random.randint(1, 25)
                        game.write_int(GetPtrAddr(game, gameModule + score_addr, score_offsets), new_score)
                    except Exception:
                        bananadropfarmlog.error("An error occurred while trying to bypass the bot idle check.")
                        continue
                time.sleep(botidlecheckbypassdelay)

    elif botidlecheckbypassmethod_var.get() == "Random value":
        def update_score():
            while botidlecheckbypass_var.get():
                for game, gameModule in game_instances:
                    try:
                        new_score = random.randint(1, 1000000)
                        game.write_int(GetPtrAddr(game, gameModule + score_addr, score_offsets), new_score)
                    except Exception:
                        bananadropfarmlog.error("An error occurred while trying to bypass the bot idle check.")
                        continue
                time.sleep(botidlecheckbypassdelay)

    elif botidlecheckbypassmethod_var.get() == "Increment":
        def update_score():
            while botidlecheckbypass_var.get():
                for game, gameModule in game_instances:
                    try:
                        current_score = game.read_int(GetPtrAddr(game, gameModule + score_addr, score_offsets))
                        new_score = current_score + 1
                        game.write_int(GetPtrAddr(game, gameModule + score_addr, score_offsets), new_score)
                    except Exception:
                        bananadropfarmlog.error("An error occurred while trying to bypass the bot idle check.")
                        continue
                time.sleep(botidlecheckbypassdelay)

    if botidlecheckbypass_var.get():
        bananadropfarmlog.info(f"Bot idle check bypass has been activated. | Method: {botidlecheckbypassmethod_var.get()} | Delay: {botidlecheckbypassdelay} seconds")
    else:
        bananadropfarmlog.info("Bot idle check bypass has been deactivated.")

    thread = threading.Thread(target=update_score)
    thread.daemon = True
    thread.start()

def spoofcps1():
    if spoofcpsdelay_var.get() != None:
        spoofcpsdelay = float(spoofcpsdelay_var.get())
    else:
       spoofcpsdelay = 0.5

    if spoofcpsmethod_var.get() == "Random":
        def update_cps():
            while spoofcps_var.get():
                for game, gameModule in game_instances:
                    try:
                        new_cps = random.randint(1, 1000000)
                        game.write_int(GetPtrAddr(game, gameModule + score_addr, score_offsets) + cps_offset, new_cps)
                    except Exception:
                        bananadropfarmlog.error("An error occurred while trying to spoof cps.")
                        continue
                time.sleep(spoofcpsdelay)

    elif spoofcpsmethod_var.get() == "Random normal":
        def update_cps():
            while spoofcps_var.get():
                for game, gameModule in game_instances:
                    try:
                        new_cps = random.randint(1, 20)
                        game.write_int(GetPtrAddr(game, gameModule + score_addr, score_offsets) + cps_offset, new_cps)
                    except Exception:
                        bananadropfarmlog.error("An error occurred while trying to spoof cps.")
                        continue
                time.sleep(spoofcpsdelay)

    elif spoofcpsmethod_var.get() == "Static":
        def update_cps():
            while spoofcps_var.get():
                for game, gameModule in game_instances:
                    try:
                        game.write_int(GetPtrAddr(game, gameModule + score_addr, score_offsets) + cps_offset, 15)
                    except Exception:
                        bananadropfarmlog.error("An error occurred while trying to spoof cps.")
                        continue
                time.sleep(spoofcpsdelay)

    if spoofcps_var.get():
        bananadropfarmlog.info(f"Cps spoof has been activated. | Method: {spoofcpsmethod_var.get()} | Delay: {spoofcpsdelay} seconds")
    else:
        bananadropfarmlog.info("Cps spoof has been deactivated.")

    thread = threading.Thread(target=update_cps)
    thread.daemon = True
    thread.start()

def idletimerreset1():
    idletimerresetdelay = 5.0

    def update_timer():
        while idletimerreset_var.get():
            for game, gameModule in game_instances:
                try:
                    game.write_float(GetPtrAddr(game, gameModule + score_addr, score_offsets) + idletimer_offset, 0.0)
                except Exception:
                    bananadropfarmlog.error("An error occurred while trying to reset idle timer.")
                    continue
            time.sleep(idletimerresetdelay)

    if idletimerreset_var.get():
        bananadropfarmlog.info(f"Idle timer reset has been activated.")
    else:
        bananadropfarmlog.info("Idle timer reset has been deactivated.")

    thread = threading.Thread(target=update_timer)
    thread.daemon = True
    thread.start()

options = customtkinter.CTkTabview(master=app, width=520, height=300)
options.pack(anchor=customtkinter.CENTER)

options.add("Cheat")
options.add("Config")
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

resetscore = customtkinter.CTkButton(master=score, text="Reset Score", command=resetscore1)
resetscore.pack(side="left", padx=5)


botidlecheckbypassall = customtkinter.CTkFrame(master=options.tab("Cheat"))
botidlecheckbypassall.pack(side="top", padx=20, pady=8)

botidlecheckbypass_var = customtkinter.BooleanVar(value=False)
botidlecheckbypass = customtkinter.CTkCheckBox(master=botidlecheckbypassall, text="Bot Idle Check Bypass", command=botidlecheckbypass1, variable=botidlecheckbypass_var)
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
spoofcps = customtkinter.CTkCheckBox(master=spoofcpsall, text="Spoof Cps", command=spoofcps1, variable=spoofcps_var)
spoofcps.pack(side="left", padx=5)

spoofcpsmethod_var = customtkinter.StringVar(value="Random normal")
spoofcpsmethod = customtkinter.CTkComboBox(master=spoofcpsall, values=["Random", "Random normal", "Static"], variable=spoofcpsmethod_var, width=150)
spoofcpsmethod.pack(side="left", padx=5)
spoofcpsmethod_var.set("Random normal")

spoofcpsdelay_var = customtkinter.StringVar(value='0.5')
spoofcpsdelay = customtkinter.CTkComboBox(master=spoofcpsall, values=['0.5', '1', '2', '5', '10', '15', '30', '45', '60', '120', '180', '300'], variable=spoofcpsdelay_var, width=60)
spoofcpsdelay.pack(side="left", padx=5)
spoofcpsdelay_var.set('0.5')


idletimerresetall = customtkinter.CTkFrame(master=options.tab("Cheat"))
idletimerresetall.pack(side="top", padx=20, pady=8)

idletimerreset_var = customtkinter.BooleanVar(value=False)
idletimerreset = customtkinter.CTkCheckBox(master=idletimerresetall, text="Idle Timer Reset", command=idletimerreset1, variable=idletimerreset_var)
idletimerreset.pack(side="left", padx=5)


saveconfig = customtkinter.CTkFrame(master=options.tab("Config"))
saveconfig.pack(side="top", padx=20, pady=8)

saveconfigname = customtkinter.CTkEntry(master=saveconfig, placeholder_text="Config name")
saveconfigname.pack(side="left", padx=5)

saveconfigtofile = customtkinter.CTkButton(master=saveconfig, text="Save config", command=save_config)
saveconfigtofile.pack(side="left", padx=5)


loadconfig = customtkinter.CTkFrame(master=options.tab("Config"))
loadconfig.pack(side="top", padx=20, pady=8)

loadconfigname_var = customtkinter.StringVar(value='example.yaml')
loadconfigname = customtkinter.CTkComboBox(master=loadconfig, values=get_configs(), variable=loadconfigname_var, width=150)
loadconfigname.pack(side="left", padx=5)
loadconfigname_var.set('example.yaml')

loadconfigfromfile = customtkinter.CTkButton(master=loadconfig, text="Load config", command=load_config)
loadconfigfromfile.pack(side="left", padx=5)


info = """Score Changer - changes score

Reset Score - resets score

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

Idle Timer Reset - resets the idle timer to 0 every 5 seconds (it is not visible in the game)

Notes: 
 - The chosen method is activated every few seconds, 
   depending on the delay you choose.
 - If you want to run more than one banana instance, 
   please use multiplesteaminstances.py to run multiple
   instances of the game.
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

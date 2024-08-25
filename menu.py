import pymem
import yaml
import psutil
import ctypes
import random
import threading
import customtkinter
import webbrowser
import datetime
import asyncio
import sys
import os

from pystyle import Colorate, Colors, Center
from colorsys import hsv_to_rgb
from pymem.process import module_from_name
from typing import Callable, Dict

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

class ThreadManager:
    def __init__(self):
        self.loop = asyncio.new_event_loop()
        self.tasks: Dict[str, asyncio.Task] = {}
        self._running = False

    async def _run_task(self, name: str, func: Callable, *args, **kwargs):
        while self._running:
            try:
                await func(*args, **kwargs)
            except Exception as e:
                bananadropfarmlog.error(f"Error in task {name}: {e}")
                await asyncio.sleep(1)

    def start_task(self, name: str, func: Callable, *args, **kwargs):
        if name in self.tasks:
            raise ValueError(f"Task {name} already exists")
        
        async def wrapped_func():
            while True:
                try:
                    if asyncio.iscoroutinefunction(func):
                        await func(*args, **kwargs)
                    else:
                        await self.loop.run_in_executor(None, func, *args, **kwargs)
                except Exception as e:
                    bananadropfarmlog.error(f"Error in task {name}: {e}")
                await asyncio.sleep(0.1)

        task = self.loop.create_task(wrapped_func())
        self.tasks[name] = task

    def stop_task(self, name: str):
        if name in self.tasks:
            self.tasks[name].cancel()
            del self.tasks[name]

    def start(self):
        self._running = True
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def stop(self):
        self._running = False
        for task in self.tasks.values():
            task.cancel()
        self.loop.stop()
        self.tasks.clear()

bananadropfarmlog = DebugLog()
thread_manager = ThreadManager()

if getattr(sys, 'frozen', False):
    try:
        ctypes.windll.kernel32.SetConsoleTitleW("Banana Drop Farm v1.7 | github.com/zZan54")

        bananadropfarm = Center.XCenter("\nBanana Drop Farm v1.7\n")
        print(Colorate.Horizontal(Colors.yellow_to_red, bananadropfarm, 1))
    except Exception:
        pass
else:
    ctypes.windll.kernel32.SetConsoleTitleW("Banana Drop Farm v1.7 | github.com/zZan54")

    bananadropfarm = Center.XCenter("\nBanana Drop Farm v1.7\n")
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
        sys.exit()

def load_menu():
    global game, gameModule, game_instances

    try:
        banana_processes = get_banana_processes()
        if len(banana_processes) == 0:
            bananadropfarmlog.error("Banana process not found. Exiting...")
            sys.exit()
        else:
            game_instances = []
            for banana_process in banana_processes:
                try:
                    game = pymem.Pymem(banana_process)
                    gameModule = module_from_name(game.process_handle, "GameAssembly.dll").lpBaseOfDll
                    game_instances.append((game, gameModule))
                    bananadropfarmlog.info(f"Successfully found the game process with PID {banana_process}.")
                except Exception:
                    bananadropfarmlog.error(f"An error occurred while trying to find the game process with PID {banana_process}.")
                    continue
    except Exception:
        bananadropfarmlog.error(f"An error occurred while trying to find the game process. Exiting...")
        sys.exit()

load_menu()

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

currently_loaded_config = None
def load_config():
    global currently_loaded_config

    config_name = loadconfigname_var.get()
    if config_name != currently_loaded_config:
        with open(f'configs/{config_name}', 'r') as config_file:
            config = yaml.safe_load(config_file)
            currently_loaded_config = config_name

        try:
            botidlecheckbypassmethod_var.set(config['botidlecheckbypass']['method'])
            botidlecheckbypassdelay_var.set(config['botidlecheckbypass']['delay'])
        except Exception:
            pass

        try:
            botidlecheckbypass_var.set(config['botidlecheckbypass']['enabled'])
            if botidlecheckbypass_var.get():
                botidlecheckbypass1()
        except Exception:
            pass

        try:
            spoofcpsmethod_var.set(config['spoofcps']['method'])
            spoofcpsdelay_var.set(config['spoofcps']['delay'])
        except Exception:
            pass

        try:
            spoofcps_var.set(config['spoofcps']['enabled'])
            if spoofcps_var.get():
                spoofcps1()
        except Exception:
            pass

        try:
            idletimerreset_var.set(config['idletimerreset']['enabled'])
            if idletimerreset_var.get():
                idletimerreset1()
        except Exception:
            pass

    else:
        bananadropfarmlog.error(f"Config {config_name} is already loaded.")
        pass

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

score_addr = 0xFC6EC0
score_offsets = [0x380, 0x40, 0x370, 0x88, 0xB8, 0x20, 0x108]
mainasset_addr = 0x1056600
mainasset_offsets = [0xD60, 0x60, 0x10, 0xF0, 0x4B4]
droptimer_addr = 0x10670C8
droptimer_offsets = [0x390, 0xD48, 0x140, 0x70, 0x20]
droptimerfix_offset = 0x4
cps_offset = 0x38
idletimer_offset = 0x34
crash_offset = 0x18

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
    if botidlecheckbypass_var.get():
        botidlecheckbypassdelay = float(botidlecheckbypassdelay_var.get() or 2.0)
        method = botidlecheckbypassmethod_var.get()

        async def update_score():
            while True:
                for game, gameModule in game_instances:
                    try:
                        if method == "Random increment":
                            current_score = game.read_int(GetPtrAddr(game, gameModule + score_addr, score_offsets))
                            new_score = current_score + random.randint(1, 25)
                        elif method == "Random value":
                            new_score = random.randint(1, 1000000)
                        elif method == "Increment":
                            current_score = game.read_int(GetPtrAddr(game, gameModule + score_addr, score_offsets))
                            new_score = current_score + 1
                        game.write_int(GetPtrAddr(game, gameModule + score_addr, score_offsets), new_score)
                    except Exception:
                        bananadropfarmlog.error("An error occurred while trying to bypass the bot idle check.")
                await asyncio.sleep(botidlecheckbypassdelay)

        thread_manager.start_task("botidlecheck", update_score)
        bananadropfarmlog.info(f"Bot idle check bypass has been activated. | Method: {method} | Delay: {botidlecheckbypassdelay} seconds")
    else:
        thread_manager.stop_task("botidlecheck")
        bananadropfarmlog.info("Bot idle check bypass has been deactivated.")

def spoofcps1():
    if spoofcps_var.get():
        spoofcpsdelay = float(spoofcpsdelay_var.get() or 0.5)
        method = spoofcpsmethod_var.get()

        async def update_cps():
            while True:
                for game, gameModule in game_instances:
                    try:
                        if method == "Random":
                            new_cps = random.randint(1, 1000000)
                        elif method == "Random normal":
                            new_cps = random.randint(1, 20)
                        elif method == "Static":
                            new_cps = 15
                        game.write_int(GetPtrAddr(game, gameModule + score_addr, score_offsets) + cps_offset, new_cps)
                    except Exception:
                        bananadropfarmlog.error("An error occurred while trying to spoof cps.")
                await asyncio.sleep(spoofcpsdelay)

        thread_manager.start_task("spoofcps", update_cps)
        bananadropfarmlog.info(f"Cps spoof has been activated. | Method: {method} | Delay: {spoofcpsdelay} seconds")
    else:
        thread_manager.stop_task("spoofcps")
        bananadropfarmlog.info("Cps spoof has been deactivated.")

def idletimerreset1():
    if idletimerreset_var.get():
        async def update_timer():
            while True:
                for game, gameModule in game_instances:
                    try:
                        game.write_float(GetPtrAddr(game, gameModule + score_addr, score_offsets) + idletimer_offset, 0.0)
                    except Exception:
                        bananadropfarmlog.error("An error occurred while trying to reset idle timer.")
                await asyncio.sleep(5.0)

        thread_manager.start_task("idletimerreset", update_timer)
        bananadropfarmlog.info("Idle timer reset has been activated.")
    else:
        thread_manager.stop_task("idletimerreset")
        bananadropfarmlog.info("Idle timer reset has been deactivated.")

def changemainasset1():
    try:
        new_mainasset = int(mainassetvalue.get())
        new_mainasset += 1

        mainassetvalue.delete(0, "end")
        mainassetvalue.insert(0, new_mainasset)
    except Exception:
        mainassetvalue.delete(0, "end")
        mainassetvalue.insert(0, 1)
        return
    
    for game, gameModule in game_instances:
        try:
            game.write_int(GetPtrAddr(game, gameModule + mainasset_addr, mainasset_offsets), new_mainasset)
            bananadropfarmlog.info(f"Successfully set the main asset to {new_mainasset}.")
        except Exception:
            bananadropfarmlog.error(f"An error occurred while trying to set the main asset to {new_mainasset}.")
            continue

def changemainasset2():
        try:
            new_mainasset = int(mainassetvalue.get())
            new_mainasset -= 1

            mainassetvalue.delete(0, "end")
            mainassetvalue.insert(0, new_mainasset)
        except Exception:
            mainassetvalue.delete(0, "end")
            mainassetvalue.insert(0, 0)
            return
        
        for game, gameModule in game_instances:
            try:
                game.write_int(GetPtrAddr(game, gameModule + mainasset_addr, mainasset_offsets), new_mainasset)
                bananadropfarmlog.info(f"Successfully set the main asset to {new_mainasset}.")
            except Exception:
                bananadropfarmlog.error(f"An error occurred while trying to set the main asset to {new_mainasset}.")
                continue

def changedroptimer():
    try:
        hours = float(droptimervaluehours.get())
        minutes = float(droptimervalueminutes.get())
        seconds = float(droptimervalueseconds.get())
    except Exception:
        bananadropfarmlog.error("Please enter a valid time value.")

        droptimervaluehours.delete(0, "end")
        droptimervaluehours.insert(0, 0)
        droptimervalueminutes.delete(0, "end")
        droptimervalueminutes.insert(0, 0)
        droptimervalueseconds.delete(0, "end")
        droptimervalueseconds.insert(0, 0)
        return
    
    new_time = (hours * 3600) + (minutes * 60) + seconds + 1
    
    for game, gameModule in game_instances:
        try:
            game.write_float(GetPtrAddr(game, gameModule + droptimer_addr, droptimer_offsets), new_time)
            bananadropfarmlog.info(f"Successfully set the drop timer to {new_time}.")
        except Exception:
            bananadropfarmlog.error(f"An error occurred while trying to set the main asset to {new_time}.")
            continue

def showlivestats1():
    global livescore, livecps, liveidletimer

    if showlivestats_var.get():
        livescore = customtkinter.CTkLabel(master=showlivestatsall, text="Live Score: ", text_color="white")
        livescore.pack(side="left", padx=5)

        livecps = customtkinter.CTkLabel(master=showlivestatsall, text="Live CPS: ", text_color="white")
        livecps.pack(side="left", padx=5)

        liveidletimer = customtkinter.CTkLabel(master=showlivestatsall, text="Live Idle Timer: ", text_color="white")
        liveidletimer.pack(side="left", padx=5)

        async def livescoreshow():
            while True:
                current_score = game.read_int(GetPtrAddr(game, gameModule + score_addr, score_offsets))
                livescore.configure(text=f"Live Score: {current_score}")
                await asyncio.sleep(1.25)

        async def livecpsshow():
            while True:
                current_cps = game.read_int(GetPtrAddr(game, gameModule + score_addr, score_offsets) + cps_offset)
                livecps.configure(text=f"Live CPS: {current_cps}")
                await asyncio.sleep(1.00)

        async def liveidletimershow():
            while True:
                current_idletimer = game.read_float(GetPtrAddr(game, gameModule + score_addr, score_offsets) + idletimer_offset)
                liveidletimer.configure(text=f"Live Idle Timer: {current_idletimer:.2f}")
                await asyncio.sleep(1.25)

        thread_manager.start_task("livescore", livescoreshow)
        thread_manager.start_task("livecps", livecpsshow)
        thread_manager.start_task("liveidletimer", liveidletimershow)
    else:
        thread_manager.stop_task("livescore")
        thread_manager.stop_task("livecps")
        thread_manager.stop_task("liveidletimer")

        livescore.destroy()
        livecps.destroy()
        liveidletimer.destroy()

def opengame1():
    try:
        os.system("start steam://run/2923300")
        bananadropfarmlog.info("Successfully opened the game.")
    except Exception:
        bananadropfarmlog.error("An error occurred while trying to open the game.")
        pass

    asyncio.run(async_opengame1())

async def async_opengame1():
    await asyncio.sleep(8)
    load_menu()

def closegame1():
    try:
        os.system("taskkill /f /im Banana.exe")
        bananadropfarmlog.info("Successfully closed the game.")
    except Exception:
        bananadropfarmlog.error("An error occurred while trying to close the game.")

def crashgame1():
    try:
        game.write_int(GetPtrAddr(game, gameModule + score_addr, score_offsets) + crash_offset, -1)
        bananadropfarmlog.info("Successfully crashed the game.")
    except Exception:
        bananadropfarmlog.error("An error occurred while trying to crash the game.")

def restartgame1():
    closegame1()
    opengame1()

def fixdroptimer1():
    try:
        game.write_int(GetPtrAddr(game, gameModule + droptimer_addr, droptimer_offsets) + droptimerfix_offset, 1)
        game.write_float(GetPtrAddr(game, gameModule + droptimer_addr, droptimer_offsets), 10800.0)
        bananadropfarmlog.info("Successfully fixed the drop timer.")
    except Exception:
        bananadropfarmlog.error("An error occurred while trying to fix the drop timer.")

def fixmainasset1():
    try:
        game.write_int(GetPtrAddr(game, gameModule + mainasset_addr, mainasset_offsets), 158)
        bananadropfarmlog.info("Successfully fixed the main asset.")
    except Exception:
        bananadropfarmlog.error("An error occurred while trying to fix the main asset.")


options = customtkinter.CTkTabview(master=app, width=520, height=300)
options.pack(anchor=customtkinter.CENTER)

options.add("Cheat")
options.add("Misc")
options.add("Config")
options.add("Info")
options.set("Cheat")


score = customtkinter.CTkFrame(master=options.tab("Cheat"))
score.pack(side="top", padx=20, pady=8)

scorechanger = customtkinter.CTkLabel(master=score, text="Score Changer:", fg_color="transparent")
scorechanger.pack(side="left", padx=5)

scorevalue = customtkinter.CTkEntry(master=score, placeholder_text="Value")
scorevalue.pack(side="left", padx=5)

setscore = customtkinter.CTkButton(master=score, text="Set Score", command=changescore, width=10)
setscore.pack(side="left", padx=5)

resetscore = customtkinter.CTkButton(master=score, text="Reset Score", command=resetscore1, width=10)
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


mainasset = customtkinter.CTkFrame(master=options.tab("Misc"))
mainasset.pack(side="top", padx=20, pady=8)

mainassetchanger = customtkinter.CTkLabel(master=mainasset, text="Main Asset Changer:", fg_color="transparent")
mainassetchanger.pack(side="left", padx=5)

setmainasset1 = customtkinter.CTkButton(master=mainasset, text="-", command=changemainasset2, width=10)
setmainasset1.pack(side="left", padx=5)

mainassetvalue = customtkinter.CTkEntry(master=mainasset, placeholder_text="Value", width=50)
mainassetvalue.pack(side="left", padx=5)

setmainasset2 = customtkinter.CTkButton(master=mainasset, text="+", command=changemainasset1, width=10)
setmainasset2.pack(side="left", padx=5)


droptimer = customtkinter.CTkFrame(master=options.tab("Misc"))
droptimer.pack(side="top", padx=20, pady=8)

droptimerchanger = customtkinter.CTkLabel(master=droptimer, text="Drop Timer Changer:", fg_color="transparent")
droptimerchanger.pack(side="left", padx=5)

droptimervaluehours = customtkinter.CTkEntry(master=droptimer, placeholder_text="Hours", width=65)
droptimervaluehours.pack(side="left", padx=5)

droptimervalueminutes = customtkinter.CTkEntry(master=droptimer, placeholder_text="Minutes", width=65)
droptimervalueminutes.pack(side="left", padx=5)

droptimervalueseconds = customtkinter.CTkEntry(master=droptimer, placeholder_text="Seconds", width=65)
droptimervalueseconds.pack(side="left", padx=5)

setdroptimer = customtkinter.CTkButton(master=droptimer, text="Set Timer", command=changedroptimer, width=10)
setdroptimer.pack(side="left", padx=5)


showlivestatsall = customtkinter.CTkFrame(master=options.tab("Misc"))
showlivestatsall.pack(side="top", padx=20, pady=8)

showlivestats_var = customtkinter.BooleanVar(value=False)
showlivestats = customtkinter.CTkCheckBox(master=showlivestatsall, text="Show Live Stats", command=showlivestats1, variable=showlivestats_var)
showlivestats.pack(side="left", padx=5)


gameoptions = customtkinter.CTkFrame(master=options.tab("Misc"))
gameoptions.pack(side="top", padx=20, pady=8)

opengame = customtkinter.CTkButton(master=gameoptions, text="Open Game", command=opengame1, width=10)
opengame.pack(side="left", padx=5)

closegame = customtkinter.CTkButton(master=gameoptions, text="Close Game", command=closegame1, width=10)
closegame.pack(side="left", padx=5)

crashgame = customtkinter.CTkButton(master=gameoptions, text="Crash Game", command=crashgame1, width=10)
crashgame.pack(side="left", padx=5)

restartgame = customtkinter.CTkButton(master=gameoptions, text="Restart Game", command=restartgame1, width=10)
restartgame.pack(side="left", padx=5)


fixoptions = customtkinter.CTkFrame(master=options.tab("Misc"))
fixoptions.pack(side="top", padx=20, pady=8)

fixdroptimer = customtkinter.CTkButton(master=fixoptions, text="Fix Drop Timer", command=fixdroptimer1, width=10)
fixdroptimer.pack(side="left", padx=5)

fixmainasset = customtkinter.CTkButton(master=fixoptions, text="Fix Main Asset", command=fixmainasset1, width=10)
fixmainasset.pack(side="left", padx=5)


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

Live Score - displays the current game score, as the game does not update the score in real time

Main Asset Changer - changes main asset

Drop Timer Changer - changes drop timer, you need to enter the time in hours, minutes and seconds

Show Live Stats - displays the current score, cps and idle timer in real time

Game Options:
    - Open Game - opens the game
    - Close Game - closes the game
    - Crash Game - crashes the game
    - Restart Game - closes and opens the game again

Fix Options:
    - Fix Drop Timer - fixes the drop timer
    - Fix Main Asset - fixes the main asset (Note: it will not work every time)

Notes: 
    - The chosen method is activated every few seconds, 
      depending on the delay you choose.
    - If you want to run more than one banana instance, 
      please use multiplesteaminstances.py to run multiple
      instances of the game.
    - Live Score updates every 1.25 seconds.
    - You need to click for the score to update.
"""
infobox = customtkinter.CTkTextbox(master=options.tab("Info"), height=230, width=460)
infobox.insert("0.0", info)
infobox.configure(state="disabled")
infobox.pack(padx=20, pady=8, anchor=customtkinter.CENTER)

githublink = customtkinter.CTkLabel(app, text="github.com/zZan54", fg_color="transparent", text_color="white")
githublink.place(x=220, y=310)
githublink.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/zZan54"))

async def githublinkanimation():
    colors = [f"#{''.join(f'{int(c * 255):02x}' for c in hsv_to_rgb(i / 360, 1, 1))}" for i in range(360)]
    i = 0
    direction = 1
    while True:
        if i >= 350:
            direction = -1
        elif i <= 50:
            direction = 1
        i += direction
        githublink.place(x=10 + i, y=310)
        githublink.configure(text_color=colors[i])
        await asyncio.sleep(0.01)

def on_close():
    thread_manager.stop()
    app.destroy()
    
thread_manager.start_task("githublink", githublinkanimation)

threading.Thread(target=thread_manager.start, daemon=True).start()

app.protocol("WM_DELETE_WINDOW", on_close)
app.mainloop()
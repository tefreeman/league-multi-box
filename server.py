import keyboard
import time

def pressAndRelease(key_str: str):
    keyboard.press_and_release(key_str)


import socket

HOST = '192.168.1.8'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            
            str_msg = data.decode("utf-8")
            
            pressAndRelease(str_msg)
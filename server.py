import keyboard
import time

def pressAndRelease(key_str: str):
    keyboard.press_and_release(key_str)

class KeyToggle:
    def __init__(self):
        self.keys = {}
        
    def add_key(self, key_str: str):
        if not self.has_key(key_str):
            self.keys[key_str] = False
    
    def trigger_key(self, key_str: str):
        self.add_key(key_str)
        
        if self.keys[key_str] is True:
            keyboard.release(key_str)
        else: 
            keyboard.press(key_str)
                
        self.keys[key_str] = not self.keys[key_str]
            
    def has_key(self, key_str: str):
        return key_str in self.keys
    
    
    

import socket

HOST = '192.168.1.7'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    key_toggle = KeyToggle()
    
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            
            str_msg = data.decode("utf-8")
            eve, msg = str_msg.split('.')
            
            if eve == 'pr':
                pressAndRelease(msg)
            elif eve == 't':
                key_toggle.trigger_key(msg)
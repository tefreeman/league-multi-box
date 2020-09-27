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
    
    
class KeyToggleGroup:
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
            self.release_all()
            time.sleep(0.10)
            keyboard.press(key_str)
                
        self.keys[key_str] = not self.keys[key_str]
    
    def release_all(self):
        for key, value in self.keys.items():
            if value:
                self.trigger_key(key)
                
    def has_key(self, key_str: str):
        return key_str in self.keys
    
    

import socket

HOST = '192.168.1.7'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    key_toggle = KeyToggleGroup()
    
    with conn:
        print('Connected by', addr)
        data_stream = ''
       
        while True:
            data = conn.recv(1024)
            
            if not data:
                break
            
            data_stream += data.decode("utf-8")
            
            print(data_stream)
            
            if data_stream[0] == '~' and data_stream[-1:] == '~':
                str_stream = data_stream.replace('~', '')    
                data_stream = ''
                
                str_arr = data_stream.split('.')
                
                if len(str_arr) == 2:
                    eve = str_arr[0]
                    msg = str_arr[1]
                else:
                    break
                
                if eve == 'pr':
                    pressAndRelease(msg)
                elif eve == 't':
                    key_toggle.trigger_key(msg)
                elif eve == 'mm':
                    x, y = msg.split(',')
                    x = int(x)
                    y = int(y)
                    mouse.move(x, y)
            else:
                break
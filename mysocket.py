#!/usr/bin/env python3
import keyboard
import socket
import time
HOST = '192.168.1.7'  # The server's hostname or IP address
PORT = 65432        # The port used by the server


class MySocket:

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                            socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self):
        self.sock.connect((HOST, PORT))

    def mysend(self, eve: str, msg: str):
        payload_bytes = str.encode(eve + '.' + msg)
        sent = self.sock.send(payload_bytes)
        if sent == 0:
            raise RuntimeError("socket connection broken")
            

    
TestSocket = MySocket()
TestSocket.connect()


time.sleep(1)

keyboard.add_hotkey('shift+q', TestSocket.mysend, args=['pr', 'q'])
keyboard.add_hotkey('shift+w', TestSocket.mysend, args=['pr','w'])
keyboard.add_hotkey('shift+e', TestSocket.mysend, args=['pr','e'])
keyboard.add_hotkey('shift+r', TestSocket.mysend, args=['pr','r'])

keyboard.add_hotkey('alt+q', TestSocket.mysend, args=['pr','ctrl+q'])
keyboard.add_hotkey('alt+w', TestSocket.mysend, args=['pr','ctrl+w'])
keyboard.add_hotkey('alt+e', TestSocket.mysend, args=['pr','ctrl+e'])
keyboard.add_hotkey('alt+r', TestSocket.mysend, args=['pr','ctrl+r'])

keyboard.add_hotkey('shift+f1', TestSocket.mysend, args=['t','f1'])
keyboard.add_hotkey('shift+f2', TestSocket.mysend, args=['t','f2'])
keyboard.add_hotkey('shift+f3', TestSocket.mysend, args=['t','f3'])
keyboard.add_hotkey('shift+f4', TestSocket.mysend, args=['t','f4'])
keyboard.add_hotkey('shift+f5', TestSocket.mysend, args=['t','f5'])

keyboard.wait()
    
#!/usr/bin/env python3
import keyboard
import mouse
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
        payload_bytes = str.encode('~' + eve + '.' + msg + '~')
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
keyboard.add_hotkey('shift+b', TestSocket.mysend, args=['pr','b'])

keyboard.add_hotkey('shift+y', TestSocket.mysend, args=['pr','y'])
keyboard.add_hotkey('shift+p', TestSocket.mysend, args=['pr','p'])


keyboard.add_hotkey('shift+z', TestSocket.mysend, args=['mc','left'])
keyboard.add_hotkey('shift+x', TestSocket.mysend, args=['mc','right'])

keyboard.add_hotkey('shift+c', TestSocket.mysend, args=['ms','c'])
keyboard.add_hotkey('`', TestSocket.mysend, args=['ms','t'])


keyboard.add_hotkey('shift+f', TestSocket.mysend, args=['pr','f'])
keyboard.add_hotkey('shift+d', TestSocket.mysend, args=['pr','d'])

keyboard.add_hotkey('shift+1', TestSocket.mysend, args=['pr','1'])
keyboard.add_hotkey('shift+2', TestSocket.mysend, args=['pr','2'])
keyboard.add_hotkey('shift+3', TestSocket.mysend, args=['pr','3'])
keyboard.add_hotkey('shift+4', TestSocket.mysend, args=['pr','4'])

keyboard.add_hotkey('alt+q', TestSocket.mysend, args=['pr','ctrl+q'])
keyboard.add_hotkey('alt+w', TestSocket.mysend, args=['pr','ctrl+w'])
keyboard.add_hotkey('alt+e', TestSocket.mysend, args=['pr','ctrl+e'])
keyboard.add_hotkey('alt+r', TestSocket.mysend, args=['pr','ctrl+r'])

keyboard.add_hotkey('shift+f1', TestSocket.mysend, args=['c','f1'])
keyboard.add_hotkey('shift+f2', TestSocket.mysend, args=['c','f2'])
keyboard.add_hotkey('shift+f3', TestSocket.mysend, args=['c','f3'])
keyboard.add_hotkey('shift+f4', TestSocket.mysend, args=['c','f4'])
keyboard.add_hotkey('shift+f5', TestSocket.mysend, args=['c','f5'])
keyboard.add_hotkey('shift+space', TestSocket.mysend, args=['tr',' '])


prev_pos = (-1, -1)
while 1:
    mouse_pos = mouse.get_position()
    
    if mouse_pos[0] == prev_pos[0] and mouse_pos[1] == prev_pos[1]:
        continue
    else:
        TestSocket.mysend('mm', str(mouse_pos[0]) + ',' + str(mouse_pos[1]))
        prev_pos = (mouse_pos[0], mouse_pos[1])
   
    time.sleep(0.05)
    
keyboard.wait()
    
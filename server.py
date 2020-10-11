import keyboard
import time
import mouse
import socket
from actions import Actions
from screen_reader import ScreenReader
from gamestate import GameState
from game_loop import GameLoop


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
    

    
def auto_heal(gs, changes):
    #print( self._is_attached, ' ', self.attach_target, ' ', self.auto_heal_enabled )
    if gs['is_attached'] is True and gs['attach_target'] is not '' and gs['auto_heal_enabled is True']:
        print('auto heal firing')
        if gs['players'][gs['attach_target']].get_hp() < 0.60:
            print('heal cast')
            Actions.press_and_release_key('e')
            
        if gs['players'][gs['attach_target']].get_hp() < 0.15:
            print('summoenr heal')
            Actions.press_and_release_key('d')
            

HOST = '192.168.1.10'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
MOUSE_STATE = False
CENTER_POS = (960,540)
AUTO_HEAL_STATE = False
game_state = GameState()
GameLoop.add_command(auto_heal)

print('added auto heal')
   
screen_reader = ScreenReader(game_state)
screen_reader.daemon = True
screen_reader.start()

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
                print('break1')
                break
            
            data_stream += data.decode("utf-8")
            
            
            if data_stream[0] == '~' and data_stream[-1:] == '~':
                commands = data_stream.split('~')
                for command_str in commands:
                    
                    if len(command_str) <= 1:
                        continue
                    
                    data_stream = ''
                    str_arr = command_str.split('.')
                
                    
                    if len(str_arr) == 2:
                        eve = str_arr[0]
                        msg = str_arr[1]
                    else:
                        print('break2')
                        print(command_str)
                        break
                    
                    if eve == 'pr':
                        pressAndRelease(msg)
                   
                    elif eve == 'c':
                        Actions.switch_champions(msg)
                        target = ''
                        if msg == 'f1':
                            target = 'top'
                        elif msg == 'f2':
                            target = 'jg'
                        elif msg == 'f3':
                            target = 'mid'
                        elif msg == 'f4':
                            target = 'adc'
                        
                        game_state.set_attach_target(target)                                
                    
                    elif eve == 'mm' and MOUSE_STATE is True:
                        x, y = msg.split(',')
                        x = int(x)
                        y = int(y)
                        mouse.move(x, y)
                    
                    elif eve == 'mc':
                        if msg == 'left':
                            mouse.click(button='left')
                        elif msg == 'right':
                            mouse.click(button='right')
                    
                    elif eve == 'ms':
                        if msg == 't':
                            MOUSE_STATE = not MOUSE_STATE
                        elif msg == 'c':
                            mouse.move(CENTER_POS[0], CENTER_POS[1])
                            MOUSE_STATE = False
                    
                    elif eve == 'ah':
                        screen_reader.toggle_auto_heal()
                        print('toggle auto heal')
                    
            else:
                print('break3')
                break
            
    
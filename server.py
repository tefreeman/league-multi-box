import keyboard
import time
import mouse
import socket
from actions import Actions
from screen_reader import ScreenReader
from gamestate import GameState
from game_loop import GameLoop
from utility import UtilityFuncs
from graphics_pos import graphics_pos
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

def flee_back(gs, changes, gameState, l):
    print(time.time() - GameLoop.old_time)
    
    if time.time() - GameLoop.old_time < 11.5:
        Actions.press_and_release_key('e')
    if time.time() - GameLoop.old_time > 12 and time.time() - GameLoop.old_time < 18:
        Actions.press_and_release_key('b')
    
    elif time.time() - GameLoop.old_time > 20:
        if gs['players'][gs['attach_target']]['alive']:
            target = gs['attach_target']
            msg = ''
            if target == 'top':
                msg = 'f1'
            if target == 'jg':
                msg = 'f2'
            if target == 'mid':
                msg = 'f3'
            if target == 'adc':
                msg = 'f4'
            Actions.switch_champions(msg)
            game_state.set_attach_target(target)     
            return 'play'
        
def init_nexus_pos(gs, changes, gameState, l):
        if UtilityFuncs.dom_color(gameState.img.getpixel(graphics_pos['minimap']['top_nexus'])) == 'b':
            gameState.nexus_pos = graphics_pos['minimap']['top_nexus']
            return 'play'
        elif UtilityFuncs.dom_color(gameState.img.getpixel(graphics_pos['minimap']['bottom_nexus'])) == 'b':
             gameState.nexus_pos = graphics_pos['minimap']['bottom_nexus']
             return 'play'
        else:
            return False

    
def auto_heal(gs, changes, gameState, l):
    #print( self._is_attached, ' ', self.attach_target, ' ', self.auto_heal_enabled )
    if gs['is_attached'] is True and gs['attach_target'] is not '' and gs['auto_heal_enabled'] is True:
        print('auto heal firing')
        if gs['players'][gs['attach_target']]['hp'] < 0.60:
            print('heal cast')
            Actions.press_and_release_key('e')
            
        if gs['players'][gs['attach_target']]['hp'] < 0.18:
            print('summoenr heal')
            Actions.press_and_release_key('d')
            

def listen_attached_player_death(gs, changes, gameState, l):
    if gs['attach_target'] is not '':
        p_alive = gs['players'][gs['attach_target']]['alive']
        p_changes_alive = changes['players'][gs['attach_target']]['alive']
        if gs['is_attached'] is False and p_alive is False and changes['is_attached'] is True and p_changes_alive is True:
            Actions.move_click(gameState.nexus_pos)
            GameLoop.old_time = time.time()
            return 'flee'
    
def listen_player_attach_changes(gs, changes, gameState, l):
    if changes['attach_target'] is True:
        return 'play'
    
HOST = '192.168.1.10'  # 192.168.1.10
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
MOUSE_STATE = False
CENTER_POS = (960,540)
AUTO_HEAL_STATE = False
game_state = GameState()

GameLoop.add_command(init_nexus_pos, 'init')
GameLoop.add_command(auto_heal, 'play')
GameLoop.add_command(flee_back, 'flee')

GameLoop.add_listener(listen_attached_player_death, 'play')
GameLoop.add_listener(listen_player_attach_changes, 'flee')
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
                        if msg == '2' or msg == '1':
                            Actions.cast_on_self(msg)
                        else:         
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
                            Actions.mouse_mov(CENTER_POS[0], CENTER_POS[1])
                            MOUSE_STATE = False
                    
                    elif eve == 'ah':
                        screen_reader.toggle_auto_heal()
                        print('toggle auto heal')
                    
            else:
                print('break3')
                break
            
    
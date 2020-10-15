import keyboard
import time
import mouse
import socket
from actions import Actions
from screen_reader import ScreenReader
from game_state import GameState
from game_loop import GameLoop
from utility import UtilityFuncs
from graphics_pos import graphics_pos
import loop_funcs


def pressAndRelease(key_str: str):
    keyboard.press_and_release(key_str)



HOST = '192.168.1.10'  # 192.168.1.10
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
MOUSE_STATE = False
CENTER_POS = (960,540)
AUTO_HEAL_STATE = False
game_state = GameState()

GameLoop.add_command(loop_funcs.init_nexus_pos, 'init')
GameLoop.add_command(loop_funcs.auto_heal, 'play')
GameLoop.add_command(loop_funcs.level_up, 'play')
GameLoop.add_command(loop_funcs.flee_back, 'flee')

GameLoop.add_listener(loop_funcs.listen_attached_player_death, 'play')
GameLoop.add_listener(loop_funcs.listen_player_attach_changes, 'flee')


print('added auto heal')
   
screen_reader = ScreenReader(game_state)
screen_reader.daemon = True
screen_reader.start()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    
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
                print(data_stream)
                break
            
    
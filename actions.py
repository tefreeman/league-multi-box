import configparser
import mouse
import keyboard
import time
import threading

class Actions:
    CENTER_POS = (960,540)
    mouse_lock = False
    def __init__(self):
        pass
    
    @staticmethod
    def mouse_mov(x, y):
        if Actions.mouse_lock is False:
            mouse.move(x, y)
    
    @staticmethod
    def press_and_release_key(key: str):
        keyboard.press_and_release(key)
     
   
    @staticmethod
    def _cast_on_self(slot: str):
        Actions.mouse_lock = True
        mouse.move(Actions.CENTER_POS[0], Actions.CENTER_POS[1] - 50)
        time.sleep(3)
        Actions.press_and_release_key(slot)
        time.sleep(1)`@`
        Actions.mouse_lock = False
    
    @staticmethod    
    def cast_on_self(slot: str):
        t = threading.Thread(target=Actions._cast_on_self, args=(slot))
        t.start()
        t.join()
        
    @staticmethod
    def move_click(mov_coords):
        Actions.mouse_lock = True
        mouse.move(mov_coords[0], mov_coords[1])
        time.sleep(0.05)
        mouse.click(button='right')
        mouse.move(mov_coords[0], mov_coords[1])
        time.sleep(0.01)
        mouse.click(button='right')
        mouse.move(mov_coords[0], mov_coords[1])
        time.sleep(0.03)
        mouse.click(button='right')
        Actions.mouse_lock = False
        
    @staticmethod
    def switch_champions(key: str):
        mouse.move(60, 980)
        time.sleep(0.03)
        Actions.press_and_release_key('w')
        time.sleep(0.12)
        keyboard.press(key)
        mouse.move(Actions.CENTER_POS[0], Actions.CENTER_POS[1] - 50)
        time.sleep(0.4)
        Actions.press_and_release_key('w')
        time.sleep(0.1)
        keyboard.release(key)
        
        
    @staticmethod
    def proc_passive():
        Actions.press_and_release_key('w')
        time.sleep(0.15)
        mouse.click(button='left')
        time.sleep(0.25)
        Actions.press_and_release_key('w')


def _move_click(mov_coords):
    mouse.move(mov_coords[0], mov_coords[1])
    time.sleep(0.05)
    mouse.click(button='right')
    mouse.move(mov_coords[0], mov_coords[1])
    time.sleep(0.01)
    mouse.click(button='right')
    mouse.move(mov_coords[0], mov_coords[1])
    time.sleep(0.03)
    mouse.click(button='right')
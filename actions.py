import configparser
import mouse
import keyboard
import time


class Actions:
    CENTER_POS = (960,540)
    def __init__(self):
        pass
    
    @staticmethod
    def press_and_release_key(key: str):
        keyboard.press_and_release(key)
        
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
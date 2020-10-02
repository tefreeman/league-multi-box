from mss import mss
from PIL import Image
from threading import Thread
import numpy as np
import time
from actions import Actions

class ScreenReader(Thread):
    def __init__(self, game_state):
        Thread.__init__(self)
        self.game_state = game_state
        self.running = True
        
    def run(self):
        # Capture entire screen
        with mss() as sct:
            monitor = sct.monitors[1]
            # mon = {"top": 800, "left": 0, "width": 280, "height": 280}
            while self.running:
                sct_img = sct.grab(monitor)
                img = Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
                #self.game_state.update(img)
                time.sleep(0.35)

    def toggle_auto_heal(self):
        self.game_state.toggle_auto_heal()
        
    def stop(self):
        self.running = False
    


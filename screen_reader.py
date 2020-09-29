from mss import mss
from PIL import Image
from threading import Thread
import numpy as np
import time
from actions import Actions

class ScreenReader(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.running = True
        
    def run(self):
        # Capture entire screen
        with mss() as sct:
            monitor = sct.monitors[1]
            # mon = {"top": 800, "left": 0, "width": 280, "height": 280}
            while self.running:
                sct_img = sct.grab(monitor)
                img = Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
                
                #print(img.getpixel((920, 380)))
                #print(img.getpixel((1015, 380)))

                val = 0
                steps = 1015 - 920
                for i in range(920, 1015):
                    if img.getpixel((i, 378))[2] > 150 and img.getpixel((i, 378))[0] < 50:
                        val += 1
                hp = val / steps
                
                if hp > 0.01 and hp < 0.50:
                    Actions.press_and_release_key('e')
                time.sleep(0.35)
                print(hp)
    
    def stop(self):
        self.running = False
    


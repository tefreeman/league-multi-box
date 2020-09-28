from mss import mss
from PIL import Image
import numpy as np
import time
def capture_screenshot():
    # Capture entire screen
    with mss() as sct:
        monitor = sct.monitors[1]
        # mon = {"top": 800, "left": 0, "width": 280, "height": 280}
        sct_img = sct.grab(monitor)
        arr = np.asarray(sct_img)
        return arr
        # Convert to PIL/Pillow Image
        # return Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')

# img = capture_screenshot()
# img.show()

np_image = capture_screenshot()
print('done')

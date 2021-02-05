import cv2 as cv
from time import time
from windowcapture import WindowCapture
import pyautogui
import numpy as np
from PIL import ImageGrab
from vision import find_click_positions


# Display streamable windows
WindowCapture.list_windows_names()

# Initialize the WindowCapture class
#wincap = WindowCapture('Steam')


loop_time = time()
while True:



    # Get screenshot
    screenshot = ImageGrab.grab()
    screenshot = np.array(screenshot)
    screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)
    #screenshot = wincap.get_screenshot()

    # cv.imshow('Computer Vision', screenshot)
    find_click_positions('amongus_red.png', screenshot, threshold=0.4, debug_mode='rectangle')

    #print(f'FPS {format(1 / (time() - loop_time))}')
    loop_time = time()

    # Press 'q' with the output window focused to exit.
    # Waits 1 ms every loop to precess key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')

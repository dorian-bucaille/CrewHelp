import cv2 as cv
import numpy as np
from time import time
from windowcapture import WindowCapture


wincap = WindowCapture('This PC')

loop_time = time()
while True:

    # Get screenshot
    screenshot = wincap.get_screenshot()

    cv.imshow('Computer Vision', screenshot)

    print(f'FPS {format(1 / (time() - loop_time))}')
    loop_time = time()

    # Press 'q' with the output window focused to exit.
    # Waits 1 ms every loop to precess key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')

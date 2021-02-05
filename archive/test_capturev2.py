import win32con
import win32gui
import win32ui
import time
import cv2 as cv
import numpy as np
from detection.visionhsv import Vision
from detection.hsvfilter import HsvFilter


# Get
def get_window(window_name):
    handle = win32gui.FindWindow(None, window_name)
    if not handle:
        raise Exception(f'{window_name} window was not found. Check if it is currently opened and retry.')
    return handle

hwnd = get_window('Among Us')

# Get the window size
window_rect = win32gui.GetWindowRect(hwnd)
x = window_rect[0]
y = window_rect[1]
w = window_rect[2] - x
h = window_rect[3] - y

# Account for the window border and title bar and cut them off
border_pixels = 8
titlebar_pixels = 30
w = w - (border_pixels * 2)
h = h - titlebar_pixels - border_pixels
cropped_x = border_pixels
cropped_y = titlebar_pixels

print(f'Width : {w}, height : {h}\n')
print(f'x : {x}, y : {y}\n')

# Set the cropped coordinates offset so we can translate screenshot images into actual screen positions
offset_x = window_rect[0] + cropped_x
offset_y = window_rect[1] + cropped_y

tracker_red = Vision('processed/red_right.png', method=cv.TM_CCOEFF_NORMED)
hwnd = win32gui.GetDesktopWindow()
tracker_red.init_control_gui()

# red HSV filter
hsv_filter = HsvFilter(0, 226, 190, 179, 255, 255, 7, 0, 77, 0)

while True:

    # time.sleep(1)
    loop_time = time.time()

    # hsv_filter = tracker_red.get_hsv_filter_from_controls()

    # screenshot = ImageGrab.grab((offset_x, offset_y, offset_x + w, offset_y + h))
    # screenshot = np.array(screenshot)
    # screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)

    # get the window image data
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0, 0), (w, h), dcObj, (x + cropped_x, y + cropped_y), win32con.SRCCOPY)

    # convert the raw data into a format opencv can read
    # dataBitMap.SaveBitmapFile(cDC, 'debug.bmp')
    signedIntsArray = dataBitMap.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (h, w, 4)

    # free resources
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())

    # drop the alpha channel, or cv.matchTemplate() will throw an error like:
    #   error: (-215:Assertion failed) (depth == CV_8U || depth == CV_32F) && type == _templ.type()
    #   && _img.dims() <= 2 in function 'cv::matchTemplate'
    img = img[..., :3]

    # make image C_CONTIGUOUS to avoid errors that look like:
    #   File ... in draw_rectangles
    #   TypeError: an integer is required (got type tuple)
    # see the discussion here:
    # https://github.com/opencv/opencv/issues/14866#issuecomment-580207109
    screenshot = np.ascontiguousarray(img)
    screenshot = cv.resize(screenshot, (320, 240), interpolation=cv.INTER_AREA)

    screenshot_delay = time.time() - loop_time
    print(f'Temps du screenshot : {screenshot_delay}')
    # Environ 0.012 sec

    processed_image = tracker_red.apply_hsv_filter(screenshot, hsv_filter)
    pr1_delay = time.time() - loop_time - screenshot_delay
    print(f'pr1 delay : {pr1_delay}')

    rectangles_red = tracker_red.find(processed_image, threshold=0.4, max_results=1)
    pr2_delay = time.time() - loop_time - pr1_delay - screenshot_delay
    print(f'pr2 delay : {pr2_delay}')

    pointsred = tracker_red.get_click_points(rectangles_red)
    pr3_delay = time.time() - loop_time - pr2_delay - pr1_delay - screenshot_delay
    print(f'pr3 delay : {pr3_delay}')

    tracker_red.draw_crosshairs(screenshot, pointsred)
    pr4_delay = time.time() - loop_time - pr3_delay - pr2_delay - pr1_delay - screenshot_delay
    print(f'pr4 delay : {pr4_delay}')

    # Display processed image
    cv.imshow('Processed', processed_image)

    # Display result image
    cv.imshow('Result screen', screenshot)

    # process_delay = time.time() - loop_time - screenshot_delay
    # print(f'Temps de recherche d\'objet : {process_delay}')
    # Environ 0.13 sec --> optimiser

    print(f'Temps de rendu total : {(time.time() - loop_time)}\n~~~~~~~~~~~')
    loop_time = time.time()

    # Press 'q' with the output window focused to exit.
    # Waits 1 ms every loop to precess key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

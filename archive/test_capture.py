import win32con
import win32gui
import win32ui
from PIL import ImageGrab
import time
import cv2 as cv
import numpy as np
from vision import find_click_positions

# Find the handle for the window we want to capture.
# If no window name is given, capture the entire screen instead.
from windowcapture import WindowCapture


window_name = 'Among Us'


hwnd = win32gui.FindWindow(None, window_name)

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

hwnd = win32gui.GetDesktopWindow()

while True:
    time.sleep(3)
    loop_time = time.time()

    #screenshot = ImageGrab.grab((offset_x, offset_y, offset_x + w, offset_y + h))
    #screenshot = np.array(screenshot)
    #screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)

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

    screenshot_delay = time.time() - loop_time
    print(f'Temps du screenshot : {screenshot_delay}')
    # Environ 0.012 sec






    points1 = find_click_positions('amongus_red_big_left.JPG', screenshot, threshold=0.5,
                                   debug_mode='rectangle', onlypoints=True)
    #print(f'Points1 : {points1}')

    points2 = find_click_positions('amongus_red_big_right.JPG', screenshot, threshold=0.5,
                                   debug_mode='rectangle', onlypoints=True)
    #print(f'Points2 : {points2}')

    pointsred = points1 + points2
    print(f'Red : {pointsred}')

    points3 = find_click_positions('amongus_blue_big_left.JPG', screenshot, threshold=0.7,
                                   debug_mode='rectangle', onlypoints=True)
    #print(f'Points3 : {points3}')
    points4 = find_click_positions('amongus_blue_big_right.JPG', screenshot, threshold=0.7,
                                   debug_mode='rectangle', onlypoints=True)
    #print(f'Points4 : {points4}')

    pointsblue = points3 + points4
    print(f'Blue : {pointsred}')

    for point in pointsred:
        # Draw the point
        cv.drawMarker(screenshot, (point[0], point[1]), color=(255, 255, 0), thickness=4,
                      markerType=cv.MARKER_CROSS)
        cv.putText(screenshot, 'red', (point[0]+15, point[1]+15), cv.FONT_HERSHEY_SIMPLEX ,
                   1, (255, 255, 0), 1, cv.LINE_AA)

    for point in pointsblue:
        # Draw the point
        cv.drawMarker(screenshot, (point[0], point[1]), color=(255, 0, 255), thickness=4,
                      markerType=cv.MARKER_SQUARE)
        cv.putText(screenshot, 'blue', (point[0] + 15, point[1] + 15), cv.FONT_HERSHEY_SIMPLEX,
                   1, (255, 0, 255), 1, cv.LINE_AA)

    # Display result image
    cv.imshow('Result screen', screenshot)

    process_delay = time.time() - loop_time - screenshot_delay
    print(f'Temps de recherche d\'objet : {process_delay}')
    # Environ 0.13 sec --> optimiser

    print(f'Temps de rendu total : {(time.time() - loop_time)}\n~~~~~~~~~~~')
    loop_time = time.time()

    # Press 'q' with the output window focused to exit.
    # Waits 1 ms every loop to precess key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

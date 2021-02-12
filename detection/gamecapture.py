import numpy as np
import win32con
import win32gui
import win32ui
import cv2 as cv


# Modified class, originally written by Ben from Learn Code By Gaming.
# https://github.com/learncodebygaming/opencv_tutorials

# Used to capture screenshots for games (optimized for fullscreen).
class GameCapture:
    # Attributes
    handle = None
    x = 0
    y = 0
    w = 0
    h = 0

    # Constructor. Sets handle and coordinates.
    def __init__(self, window_name=None):

        self.handle = self.get_window_handle(window_name)
        self.set_coordinates()

    # Get the handle from a given window name. If no window name is given, return the entire screen.
    def get_window_handle(self, window_name=None):

        if window_name is None:
            self.handle = win32gui.GetDesktopWindow()
        else:
            self.handle = win32gui.FindWindow(None, window_name)
        if not self.handle:
            print(f'{window_name} window was not found. Check if it is currently opened and retry.')
            raise FileNotFoundError
        return self.handle

    # Set the window coordinates and size
    def set_coordinates(self):
        window_rect = win32gui.GetWindowRect(self.handle)
        self.x = window_rect[0]
        self.y = window_rect[1]
        self.w = window_rect[2] - self.x
        self.h = window_rect[3] - self.y

    # Get the window screenshot
    def get_screenshot(self, width=None, height=None):

        # Get the window image data
        wDC = win32gui.GetWindowDC(self.handle)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (self.x, self.y), win32con.SRCCOPY)

        # Convert the raw data into a format opencv can read
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.frombuffer(signedIntsArray, dtype='uint8')
        img.shape = (self.h, self.w, 4)

        # Drop the alpha channel
        img = img[..., :3]

        # Make image C_CONTIGUOUS
        screenshot = np.ascontiguousarray(img)

        # Resize if corresponding parameters are given
        if width and height:
            screenshot = cv.resize(screenshot, (width, height))

        # Free resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.handle, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        return screenshot

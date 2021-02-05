import cv2 as cv
from visionhsv import Vision
from hsvfilter import HsvFilter
from gamecapture import GameCapture


# This script would not exist without the excellent work of Ben from Learn Code By Gaming.
# Go check him out ! https://www.youtube.com/c/LearnCodeByGaming
# Huge thanks to him for making coding fun :)

# Set coordinates of Among Us window
amongus_screenshot = GameCapture('Among Us')

# Set handle to full screen
# We are doing this because recording game windows does not work with the win32 library (freezes on first frame)
amongus_screenshot.get_window_handle()

# Initialize variables
colors = ["red", "blue", "green", "pink", "orange", "yellow", "black", "white", "purple", "brown", "cyan",
          "lime"]
trackers = {}
processed_images = {}
rectangles = {}
points = {}
thresholds = {}

# Initialize player trackers and variables
for color in colors:
    trackers.update({color: Vision('img/' + color + '_small.png')})
    processed_images.update({color: None})
    rectangles.update({color: None})
    points.update({color: None})
    thresholds.update({color: 0.5})

# Threshold adjustments for specific colors
thresholds["green"] = 0.4
thresholds["pink"] = 0.4
thresholds["orange"] = 0.4  # black and brown detected @upper/lower engine (+ vents for black)
thresholds["yellow"] = 0.5  # yellow not so good (@shields for example)
thresholds["black"] = 0.61
thresholds["white"] = 0.4
thresholds["purple"] = 0.4
thresholds["brown"] = 0.6  # brown detected over orange, overall bad accuracy for brown
thresholds["cyan"] = 0.45
thresholds["lime"] = 0.4  # lime detected over green and vice-versa

# HSV filters to be applied
filters = {
    "red": HsvFilter(0, 229, 0, 0, 255, 255, 0, 0, 0, 0),
    "blue": HsvFilter(114, 221, 0, 119, 255, 255, 0, 0, 0, 0),
    "green": HsvFilter(64, 215, 0, 78, 255, 255, 0, 0, 0, 0),
    "pink": HsvFilter(146, 160, 0, 161, 255, 255, 0, 0, 0, 0),
    "orange": HsvFilter(6, 219, 0, 20, 255, 255, 0, 0, 0, 0),
    "yellow": HsvFilter(19, 160, 0, 31, 255, 255, 0, 0, 0, 0),
    "black": HsvFilter(104, 48, 0, 116, 63, 83, 0, 0, 0, 0),
    "white": HsvFilter(108, 22, 176, 113, 95, 255, 0, 0, 0, 0),
    "purple": HsvFilter(129, 190, 0, 134, 255, 255, 0, 0, 0, 0),
    "brown": HsvFilter(6, 184, 0, 18, 255, 255, 0, 0, 0, 0),
    "cyan": HsvFilter(83, 198, 0, 95, 255, 255, 0, 0, 0, 0),
    "lime": HsvFilter(52, 182, 0, 70, 255, 255, 0, 0, 0, 0)
}

while True:

    # Get current frame and resize it so the process is faster
    screenshot = amongus_screenshot.get_screenshot(256, 144)

    # Get detected points for every color
    for color in colors:
        processed_images[color] = trackers[color].apply_hsv_filter(screenshot, filters[color])
        rectangles[color] = trackers[color].find(processed_images[color], threshold=thresholds[color], max_results=1)
        points[color] = trackers[color].get_click_points(rectangles[color])

    # Draw a cross and write the color detected for every color
    for color in colors:
        trackers[color].draw_crosshairs(screenshot, points[color], (0, 255, 0))
        if len(points[color]):
            cv.putText(screenshot, color, (points[color][0][0] + 1, points[color][0][1] - 1), cv.FONT_HERSHEY_PLAIN,
                       0.7, (0, 255, 0), 1, cv.LINE_AA)

    # Display result image
    cv.imshow('Tracking screen', cv.resize(screenshot, (1280, 720)))

    # Press 'q' with the output window focused to exit.
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

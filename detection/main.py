import cv2 as cv
from visionhsv import Vision
from hsvfilter import HsvFilter
from gamecapture import GameCapture
from time import time
import keyboard

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
rooms = ["cafeteria", "medbay", "upper_engine", "reactor", "security", "lower_engine", "electrical", "storage", "admin",
         "communications", "shields", "navigation", "o2", "weapons"]
trackers = {}
processed_images = {}
rectangles = {}
points = {}
thresholds = {}
positions = {}
timings = {}
last_seen = {}
current_room = None

# Initialize player trackers
for color in colors:
    trackers.update({color: Vision('img/' + color + '_small.png')})
    processed_images.update({color: None})
    rectangles.update({color: None})
    points.update({color: None})
    thresholds.update({color: 0.5})
    positions.update({color: None})
    timings.update({color: None})
    last_seen.update({color: None})

# Initialize room trackers
for room in rooms:
    trackers[room] = Vision('img/' + room + '.png')
    processed_images.update({room: None})
    rectangles.update({room: None})
    points.update({room: None})

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
thresholds["room"] = 0.72  # cafeteria + o2 problem, communications + o2 problem : crop beginning of word

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
    "lime": HsvFilter(52, 182, 0, 70, 255, 255, 0, 0, 0, 0),
    "room": HsvFilter(0, 0, 0, 0, 0, 255, 0, 0, 0, 0)
}

while True:
    current_room = None
    # filters["room"] = trackers["room"].get_hsv_filter_from_controls()

    # Get current frame and resize it so the process is faster
    screenshot = amongus_screenshot.get_screenshot(256, 144)

    # Detect room
    for room in rooms:
        processed_images[room] = trackers[room].apply_hsv_filter(screenshot, filters["room"])
        rectangles[room] = trackers[room].find(processed_images[room], threshold=thresholds["room"], max_results=1)
        points[room] = trackers[room].get_click_points(rectangles[room])
        if len(points[room]):
            current_room = room

    # Get detected points for every color
    for color in colors:
        processed_images[color] = trackers[color].apply_hsv_filter(screenshot, filters[color])
        rectangles[color] = trackers[color].find(processed_images[color], threshold=thresholds[color], max_results=1)
        points[color] = trackers[color].get_click_points(rectangles[color])

        # Update player location
        if len(points[color]):
            positions[color] = current_room
            timings[color] = time()

    # Draw a cross and write the color detected for every color
    for color in colors:
        trackers[color].draw_crosshairs(screenshot, points[color], (0, 255, 0))
        if len(points[color]):
            cv.putText(screenshot, color, (points[color][0][0] + 1, points[color][0][1] - 1), cv.FONT_HERSHEY_PLAIN,
                       0.7, (0, 255, 0), 1, cv.LINE_AA)

    # Display processed image
    # cv.imshow('Processed screen', processed_images[room])

    # Display result image
    # cv.imshow('Tracking screen', cv.resize(screenshot, (1280, 720)))

    # Meeting detected
    # Press 't' to simulate this scenario
    if keyboard.is_pressed('t'):
        time_now = time()
        for color in colors:
            if timings[color]:
                last_seen[color] = time_now - timings[color]
        break

# Print last positions of encountered players.
for color in colors:
    if last_seen[color] and positions[color]:
        if int(last_seen[color]) == 0 or int(last_seen[color]) == 1:
            print(f'{color} last seen {int(last_seen[color])} second ago in {positions[color]}.')
        else:
            print(f'{color} last seen {int(last_seen[color])} seconds ago in {positions[color]}.')
    elif last_seen[color]:
        if int(last_seen[color]) == 0 or int(last_seen[color]) == 1:
            print(f'{color} last seen {int(last_seen[color])} second ago.')
        else:
            print(f'{color} last seen {int(last_seen[color])} seconds ago.')
    else:
        print(f'{color} not seen.')

print('Done.')

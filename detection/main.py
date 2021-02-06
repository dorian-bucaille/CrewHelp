import cv2 as cv
from visionhsv import Vision
from hsvfilter import HsvFilter
from gamecapture import GameCapture
from time import time
from gui.map import Map

# Debugging parameters
detectionscreen = False  # Display detection screen
processedscreen = None  # Display processed image
hsv_sliders = False  # Display GUI for HSV processing


# Create and initialize variables
colors = ["red", "blue", "green", "pink", "orange", "yellow", "black", "white", "purple", "brown", "cyan",
          "lime"]
rooms = ["cafeteria", "medbay", "upper_engine", "reactor", "security", "lower_engine", "electrical", "storage", "admin",
         "communications", "shields", "navigation", "o2", "weapons"]

trackers, processed_images, rectangles, points, thresholds, positions, timings, last_seen = {}, {}, {}, {}, {}, {}, {}, \
                                                                                            {}


# Initialize trackers
def init_trackers(tracked_obj, pos=False):
    if type(tracked_obj) == list:
        for t in tracked_obj:
            trackers.update({t: Vision('img/' + t + '.png')})
            processed_images.update({t: None})
            rectangles.update({t: None})
            points.update({t: None})
            thresholds.update({t: 0.5})
            if pos:
                positions.update({t: None})
                timings.update({t: None})
                last_seen.update({t: None})
    else:
        trackers.update({tracked_obj: Vision('img/' + tracked_obj + '.png')})
        processed_images.update({tracked_obj: None})
        rectangles.update({tracked_obj: None})


# Return True if an event has been triggered
def event_detected(screencapture, tracker, imgfilter, threshold=0.5, getrectangle=False):
    processedimg = tracker.apply_hsv_filter(screencapture, imgfilter)
    rectangle = tracker.find(processedimg, threshold=threshold, max_results=1)
    if len(rectangle):
        if getrectangle:
            return rectangle
        else:
            return True
    else:
        return False


# Print last positions of encountered players.
def print_positions():
    print('--- Recap ---')
    for col in colors:
        if last_seen[col] and positions[col]:
            if int(last_seen[col]) == 0 or int(last_seen[col]) == 1:
                print(f'{col} last seen {int(last_seen[col])} second ago in {positions[col]}.')
            else:
                print(f'{col} last seen {int(last_seen[col])} seconds ago in {positions[col]}.')
        elif last_seen[col]:
            if int(last_seen[col]) == 0 or int(last_seen[col]) == 1:
                print(f'{col} last seen {int(last_seen[col])} second ago.')
            else:
                print(f'{col} last seen {int(last_seen[col])} seconds ago.')
        else:
            print(f'{col} not seen.')


# Initialize color, room and meeting trackers
init_trackers(colors, pos=True)
init_trackers(rooms)
init_trackers('meeting')

# Threshold adjustments for specific colors
thresholds["red"] = 0.5  # Seems OK
thresholds["green"] = 0.5  # OK
thresholds["pink"] = 0.4
thresholds["orange"] = 0.4  # OK
thresholds["yellow"] = 0.53  # OK but not 100% accurate. Had to lower threshold because of empty bin storage task.
thresholds["black"] = 0.5  # OK
thresholds["white"] = 0.4
thresholds["purple"] = 0.4
thresholds["brown"] = 0.45  # OK
thresholds["cyan"] = 0.45
thresholds["lime"] = 0.3  # OK
thresholds["room"] = 0.72  # OK

# BGR for every color
bgr_colors = {
    "red": (0, 0, 255),
    "blue": (255, 0, 0),
    "green": (0, 255, 0),
    "pink": (255, 0, 255),
    "orange": (0, 127, 255),
    "yellow": (0, 255, 255),
    "black": (255, 255, 255),
    "white": (0, 0, 0),
    "purple": (191, 0, 191),
    "brown": (20, 70, 120),
    "cyan": (255, 255, 0),
    "lime": (0, 255, 0)
}

# HSV filters to be applied
filters = {
    "red": HsvFilter(0, 229, 0, 179, 237, 255, 0, 0, 255, 0),
    "blue": HsvFilter(114, 221, 0, 119, 255, 255, 0, 0, 0, 0),
    "green": HsvFilter(67, 218, 0, 76, 222, 255, 0, 0, 0, 0),
    "pink": HsvFilter(146, 160, 0, 161, 255, 255, 0, 0, 0, 0),
    "orange": HsvFilter(6, 219, 0, 20, 255, 255, 0, 0, 0, 0),
    "yellow": HsvFilter(19, 164, 184, 30, 213, 255, 0, 0, 0, 0),
    "black": HsvFilter(104, 49, 36, 116, 55, 255, 0, 0, 255, 0),
    "white": HsvFilter(108, 22, 176, 113, 95, 255, 0, 0, 0, 0),
    "purple": HsvFilter(129, 190, 0, 134, 255, 255, 0, 0, 0, 0),
    "brown": HsvFilter(6, 186, 0, 17, 198, 255, 0, 0, 255, 0),
    "cyan": HsvFilter(83, 198, 0, 95, 255, 255, 0, 0, 0, 0),
    "lime": HsvFilter(55, 193, 0, 56, 194, 255, 0, 0, 255, 0),
    "room": HsvFilter(0, 0, 0, 0, 0, 255, 0, 0, 0, 0),
    "meeting": HsvFilter(0, 0, 209, 179, 255, 255, 0, 0, 0, 0)
}

# Set coordinates of Among Us window
amongus_screenshot = GameCapture('Among Us')

# Set handle to full screen
# We are doing this because recording game windows does not work with the win32 library (freezes on first frame)
amongus_screenshot.get_window_handle()

# Init HSV GUI
if hsv_sliders:
    trackers[processedscreen].init_control_gui()

while True:
    # Reset current room
    current_room = None

    # Get current frame and resize it so the process is faster
    screenshot = amongus_screenshot.get_screenshot(256, 144)

    # Detect room
    for room in rooms:
        if event_detected(screenshot, trackers[room], filters['room'], threshold=thresholds['room']):
            current_room = room
            if detectionscreen:
                rectangles[room] = event_detected(screenshot, trackers[room], filters['room'],
                                                  threshold=thresholds['room'], getrectangle=True)
                points[room] = trackers[room].get_click_points(rectangles[room])
                cv.putText(screenshot, room, (points[room][0][0] + 1, points[room][0][1] - 1),
                           cv.FONT_HERSHEY_PLAIN, 0.7, (255, 255, 255), 1, cv.LINE_AA)

    # If in a room, detect players
    if current_room:
        for color in colors:
            # Check if color is detected
            rectangles[color] = event_detected(screenshot, trackers[color], filters[color], threshold=thresholds[color],
                                               getrectangle=True)
            # If so, update position and timing
            if rectangles[color] is not False:
                positions[color] = current_room
                timings[color] = time()

                # Draw a cross and write the color detected for every color
                if detectionscreen:
                    points[color] = trackers[color].get_click_points(rectangles[color])
                    trackers[color].draw_crosshairs(screenshot, points[color], bgr_colors[color])
                    cv.putText(screenshot, color, (points[color][0][0] + 1, points[color][0][1] - 1),
                               cv.FONT_HERSHEY_PLAIN, 0.7, bgr_colors[color], 1, cv.LINE_AA)

    # Display detection screen
    if detectionscreen:
        if processedscreen:
            if hsv_sliders:
                filters[processedscreen] = trackers[processedscreen].get_hsv_filter_from_controls()
            processed = trackers[processedscreen].apply_hsv_filter(screenshot, filters[processedscreen])
            cv.imshow('CrewHelp processed screen', processed)
            cv.waitKey(1)
        cv.imshow('CrewHelp tracking screen', cv.resize(screenshot, (1280, 720)))
        cv.waitKey(1)

    # Get out of loop if a meeting is detected
    if event_detected(screenshot, trackers['meeting'], filters['meeting'], threshold=0.5):
        print("--- Meeting detected ! ---\n")
        cv.destroyAllWindows()
        time_now = time()
        for color in colors:
            if timings[color]:
                last_seen[color] = time_now - timings[color]
        break

# Print last positions of encountered players.
print_positions()

# Display map and markers
actual_map = Map(positions, last_seen)
actual_map.set_markers()
actual_map.display_markers()
actual_map.display_map()

exit(0)

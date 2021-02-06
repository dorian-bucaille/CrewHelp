import cv2 as cv
from visionhsv import Vision
from gamecapture import GameCapture
from time import time
from gui.map import Map
import cons.cst

# Debugging parameters
detectionscreen = False  # Display detection screen
processedscreen = None  # Display processed image
hsv_sliders = False  # Display GUI for HSV processing


# Create and initialize variables
colors = cons.cst.colors
rooms = cons.cst.rooms

trackers, processed_images, rectangles, points, positions, timings, last_seen = {}, {}, {}, {}, {}, {}, {}


# Initialize trackers
def init_trackers(tracked_obj, pos=False):
    if type(tracked_obj) == list:
        for t in tracked_obj:
            trackers.update({t: Vision('img/' + t + '.png')})
            processed_images.update({t: None})
            rectangles.update({t: None})
            points.update({t: None})
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

# Set detection thresholds
thresholds = cons.cst.thresholds

# BGR for every color
bgr_colors = cons.cst.bgr_colors

# HSV filters to be applied
filters = cons.cst.filters

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

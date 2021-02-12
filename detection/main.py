import cv2 as cv
from visionhsv import Vision
from gamecapture import GameCapture
from time import time
import cons.cst
import gui.qtmap
import gui.qtgui
import threading
import logging

# Logger initialization
amongus_screenshot = None
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("CrewHelp logger")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler("logs.log")
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s - %(asctime)s : %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.debug("Logger initialized.")

# Debugging parameters
detectionscreen = False  # Display detection screen
processedscreen = None  # Display processed image
hsv_sliders = False  # Display GUI for HSV processing

# Size of the processed frames (the smallest the fastest)
resized_x = 256
resized_y = 144

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
            print(f'{col} not seen in a room.')
    print('')


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

logger.debug("Variables initialized.")

# Set coordinates of Among Us window
try:
    amongus_screenshot = GameCapture('Among Us')
except FileNotFoundError:
    logger.error("Among Us window was not found.")
    exit(1)
logger.info("Among Us window was found.")

# Set handle to full screen
# We are doing this because recording game windows does not work with the win32 library (freezes on first frame)
amongus_screenshot.get_window_handle()

# Init HSV GUI
if hsv_sliders:
    trackers[processedscreen].init_control_gui()
    logger.debug("GUI for HSV filter sliders initialized.")


def main_program():

    # Detection loop
    logger.debug("Starting detection loop...")

    last_visited_room = None
    while True:

        # Check if game is still opened
        try:
            GameCapture('Among Us')
        except FileNotFoundError:
            logger.error("Among Us window was closed.")
            exit(2)
        logger.debug("Among Us window was found.")

        # Reset current room
        current_room = None
        logger.debug("Room reset.")

        # Get current frame and resize it so the process is faster
        screenshot = amongus_screenshot.get_screenshot(resized_x, resized_y)
        logger.debug(f"Frame has been resized to ({resized_x}, {resized_y}).")

        # Detect room
        logger.debug("Starting room detection...")
        for room in rooms:
            logger.debug(f"Room to be detected : {room}.")
            if event_detected(screenshot, trackers[room], filters['room'], threshold=thresholds['room']):
                current_room = room
                if last_visited_room != current_room:
                    logger.info(f"Current room is now {room}.")
                if detectionscreen:
                    rectangles[room] = event_detected(screenshot, trackers[room], filters['room'],
                                                      threshold=thresholds['room'], getrectangle=True)
                    points[room] = trackers[room].get_click_points(rectangles[room])
                    cv.putText(screenshot, room, (points[room][0][0] + 1, points[room][0][1] - 1),
                               cv.FONT_HERSHEY_PLAIN, 0.7, (255, 255, 255), 1, cv.LINE_AA)
                    logger.debug(f"Updated marker and text for {room}.")
                last_visited_room = current_room
        logger.debug("Room detection ended.")

        # If in a room, detect players
        logger.debug("Starting color detection...")
        if current_room:
            for color in colors:
                logger.debug(f"Color to be detected : {color}.")

                # Check if color is detected
                rectangles[color] = event_detected(screenshot, trackers[color], filters[color],
                                                   threshold=thresholds[color],
                                                   getrectangle=True)

                # If so, update position and timing
                if rectangles[color] is not False:
                    positions[color] = current_room
                    timings[color] = time()
                    logger.info(f"Color {color} detected in {current_room} !")
                    logger.debug(f"Updated {color} position to {current_room} (last seen timing was reset).")

                    # Draw a cross and write the color detected for every color
                    if detectionscreen:
                        points[color] = trackers[color].get_click_points(rectangles[color])
                        trackers[color].draw_crosshairs(screenshot, points[color], bgr_colors[color])
                        cv.putText(screenshot, color, (points[color][0][0] + 1, points[color][0][1] - 1),
                                   cv.FONT_HERSHEY_PLAIN, 0.7, bgr_colors[color], 1, cv.LINE_AA)
                        logger.debug(f"Updated marker and text for {color} in ({points[color][0][0]},"
                                     f"{points[color][0][1]}).")
        logger.debug("Color detection ended...")

        # Display detection screen
        if detectionscreen:
            if processedscreen:
                if hsv_sliders:
                    filters[processedscreen] = trackers[processedscreen].get_hsv_filter_from_controls()
                processed = trackers[processedscreen].apply_hsv_filter(screenshot, filters[processedscreen])
                cv.imshow('CrewHelp processed screen', cv.resize(processed, (1176, 664)))
                cv.waitKey(1)
            cv.imshow('CrewHelp tracking screen', cv.resize(screenshot, (1176, 664)))
            cv.waitKey(1)
            logger.debug("Detection screen updated.")

        # Get out of loop if a meeting is detected
        if event_detected(screenshot, trackers['meeting'], filters['meeting'], threshold=0.5):
            logger.info("Meeting detected !")
            cv.destroyAllWindows()
            time_now = time()
            for color in colors:
                if timings[color]:
                    last_seen[color] = time_now - timings[color]
            logger.debug("Exiting detection loop...")
            break

    # Print last positions of encountered players.
    logger.info(f"{print_positions()}")

    # Display map and markers
    logger.info("Displaying map...")
    gui.qtmap.display(positions, last_seen)
    logger.info("Map closed.")


logger.info("All variables and functions have been initialized.")
logger.info("Starting program.")
main_loop_thread = threading.Thread(target=main_program)

while True:
    main_loop_thread.start()
    logger.debug("Main loop thread started.")
    main_loop_thread.join()
    logger.debug("Main loop thread ended.")

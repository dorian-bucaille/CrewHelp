import cv2 as cv
import numpy as np


def find_click_positions(needle_img_path, haystack_img, threshold=0.7, debug_mode=None, method=cv.TM_CCOEFF_NORMED,
                         needlepack=[], onlypoints=False):
    if not isinstance(needle_img_path, list):
        needlepack.append(needle_img_path)
    elif isinstance(needle_img_path, list):
        needlepack = needle_img_path

    for needle in needlepack:
        # Open the needle (part of the haystack that we want to identify)
        needle_img = cv.imread(needle, cv.IMREAD_UNCHANGED)

        # Get dimensions of the needle image
        needle_w = needle_img.shape[1]
        needle_h = needle_img.shape[0]

        # Search for the needle in the haystack
        result = cv.matchTemplate(haystack_img, needle_img, method)

        # Get locations with a score greater than the threshold
        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))

        # Convert locations to rectangles
        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), needle_w, needle_h]
            rectangles.append(rect)

        rectangles, weights = cv.groupRectangles(rectangles, 1, 0.5)

        points = []

        if len(rectangles):

            # Loop over all the locations and draw their rectangles
            for (x, y, w, h) in rectangles:

                # Determine the center position
                center_x = x + int(w / 2)
                center_y = y + int(h / 2)
                # Save the point
                points.append((center_x, center_y))

                if debug_mode == 'rectangle':
                    # Determine the rectangle position
                    top_left = (x, y)
                    bottom_right = (x + w, y + h)
                    # Draw the rectangle
                    cv.rectangle(haystack_img, top_left, bottom_right, color=(255, 0, 255), thickness=2, lineType=cv.LINE_4)

                elif debug_mode == 'points':
                    # Draw the point
                    cv.drawMarker(haystack_img, (center_x, center_y), color=(255, 0, 255), thickness=4,
                                  markerType=cv.MARKER_CROSS)

        if debug_mode and not onlypoints:
            # Display result image
            cv.imshow('Matches', haystack_img)
            # cv.waitKey()
            # Save result image
            # cv.imwrite('result.png', haystack_img)

    return points

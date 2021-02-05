import cv2 as cv
import numpy as np


# Improved version of main2.py. Can now detect multiple similar parts of an image and draw a rectangle over them.
# Is now a function.

def findClickPositions(needle_img_path, haystack_img_path, threshold=0.7, debug_mode=None, method=cv.TM_CCOEFF_NORMED):
    # Open the haystack (full image) and the needle (part of the haystack that we want to identify)
    haystack_img = cv.imread(haystack_img_path, cv.IMREAD_REDUCED_COLOR_2)
    needle_img = cv.imread(needle_img_path, cv.IMREAD_REDUCED_COLOR_2)

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
                cv.rectangle(haystack_img, top_left, bottom_right, color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)

            elif debug_mode == 'points':
                # Draw the point
                cv.drawMarker(haystack_img, (center_x, center_y), color=(255, 0, 255), thickness=4,
                              markerType=cv.MARKER_CROSS)
        if debug_mode:
            # Display result image
            cv.imshow('Matches', haystack_img)
            cv.waitKey()
            # Save result image
            # cv.imwrite('result.png', haystack_img)

    return points


points = findClickPositions('amongus_medbay_bed.png', 'amongus_medbay.png', debug_mode='rectangle')
print(points)

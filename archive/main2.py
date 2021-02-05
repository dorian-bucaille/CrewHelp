import cv2 as cv
import numpy as np

# Improved version of main1.py. Can now detect multiple similar parts of an image and draw a rectangle over them.

# Open the haystack (full image) and the needle (part of the haystack that we want to identify)
haystack_img = cv.imread('amongus_medbay.png', cv.IMREAD_REDUCED_COLOR_2)
needle_img = cv.imread('amongus_medbay_bed.png', cv.IMREAD_REDUCED_COLOR_2)

# Search for the needle in the haystack
result = cv.matchTemplate(haystack_img, needle_img, cv.TM_CCOEFF_NORMED)
# print(result)

threshold = 0.7
locations = np.where(result >= threshold)
# The np.where value will look like this :
# (array([1,5], dtype=int32), array([1,15], dtype=int32))
# print(locations)

# We can zip those up into tuples
locations = list(zip(*locations[::-1]))

if locations:
    print(f'Found needle(s) at these locations :\n{locations}\n')
    # Get dimensions of the needle image
    needle_w = needle_img.shape[1]
    needle_h = needle_img.shape[0]

    # Loop over all the locations and draw their rectangles
    for loc in locations:
        # Determine the rectangle positions
        top_left = loc
        bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)

        # Draw the rectangle
        cv.rectangle(haystack_img, top_left, bottom_right, color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)

    # Display result image
    cv.imshow('Matches', haystack_img)
    cv.waitKey()

    # Save result image
    # cv.imwrite('result.png', haystack_img)

else:
    print('Needle not found.')

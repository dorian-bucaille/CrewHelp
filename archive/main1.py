import cv2 as cv

# Basic object detection script using opencv. Can detect a portion of an image and draw a rectangle over it.

# Open the haystack (full image) and the needle (part of the haystack that we want to identify)
haystack_img = cv.imread('amongus_medbay.png', cv.IMREAD_REDUCED_COLOR_2)
needle_img = cv.imread('amongus_medbay_redcross.png', cv.IMREAD_REDUCED_COLOR_2)

# Search for the needle in the haystack
result = cv.matchTemplate(haystack_img, needle_img, cv.TM_CCOEFF_NORMED)

# Get the best match position
_, max_val, _, max_loc = cv.minMaxLoc(result)

print(f'Best match top left position : {max_loc}\n')
print(f'Best match confidence : {max_val}\n')

threshold = 0.8
if max_val >= threshold:
    print('Found needle.')

    # Get dimensions of the needle image
    needle_w = needle_img.shape[1]
    needle_h = needle_img.shape[0]

    # Draw rectangle on the needle
    top_left = max_loc
    bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)
    cv.rectangle(haystack_img, top_left, bottom_right, color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)

    # Display result image
    cv.imshow('Result', haystack_img)
    cv.waitKey()

    # Save result image
    # cv.imwrite('result.png', haystack_img)

else:
    print('Needle not found.')

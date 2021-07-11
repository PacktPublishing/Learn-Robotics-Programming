from __future__ import print_function

import cv2
import numpy as np

from matplotlib import pyplot as plt

# This is so we can use matplot lib to see our images
def plot_image(position, img):
    plt.subplot(position)
    plt.gca().tick_params('x', which='both', bottom=False, top=False, labelbottom=False)
    plt.gca().tick_params('y', which='both', left=False, right=False, labelleft=False)
    plt.imshow(img)

plt.figure(1)

# load an image
original_frame = cv2.imread("test_images/green_pin.jpg", cv2.IMREAD_COLOR)

im_rgb = cv2.cvtColor(original_frame, cv2.COLOR_BGR2RGB)
plot_image(231, im_rgb)


# Convert to hsv
frame_hsv = cv2.cvtColor(original_frame, cv2.COLOR_BGR2HSV)
plot_image(232, frame_hsv)

# Mask it to our desired color
low_range = (25, 70, 25)
high_range = (80, 255, 255)

masked = cv2.inRange(frame_hsv, low_range, high_range)
plot_image(233, masked)

# Find the contours of the image (outline points)
contour_image = np.copy(masked)
contours, _ = cv2.findContours(contour_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

display_contours = np.copy(im_rgb)
cv2.drawContours(display_contours, contours, -1, (0, 255, 0), 3)
plot_image(234, display_contours)

# Get the circles
# Find enclosing circles
circles = [cv2.minEnclosingCircle(cnt) for cnt in contours]

display_outline = np.copy(im_rgb)
for (x, y), radius in circles:
    cv2.circle(display_outline, (int(x), int(y)), int(radius), [255, 0, 0])

plot_image(235, display_outline)
plt.show()







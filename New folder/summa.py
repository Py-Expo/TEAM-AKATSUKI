import cv2 as cv
import numpy as np

def detect_lanes(image):
    # Convert the image to grayscale
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise and help edge detection
    blurred = cv.GaussianBlur(gray, (11,11), 0)

    inverted_image = cv.bitwise_not(blurred)

    # Apply Canny edge detection with adaptive thresholds
    edges = cv.Canny(inverted_image, 200, 150)

    # Define region of interest (ROI)
    height, width = edges.shape
    roi_vertices = [(0, height), (width // 2, height // 2), (width, height)]
    mask = np.zeros_like(edges)
    cv.fillPoly(mask, [np.array(roi_vertices, np.int32)], 255)
    masked_edges = cv.bitwise_and(edges, mask)

    # Apply Hough Transform to detect lines with adjusted parameters
    lines = cv.HoughLinesP(masked_edges, 1, np.pi / 180, threshold=10, minLineLength=200, maxLineGap=300)

    # Draw detected lines on the original image
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv.line(image, (x1, y1), (x2, y2), (0, 255, 0), 5)

    # Draw blue lane area
        # Get the end points of the green lane lines
    left_x1, left_y1, left_x2, left_y2 = lines[0][0]
    right_x1, right_y1, right_x2, right_y2 = lines[1][0]

    # Define the bottom corners of the blue lane area
    # Define the bottom corners of the blue lane area
    # Define the bottom corners of the blue lane area
    bottom_left = (left_x1, left_y1)
    bottom_right = (right_x1, right_y1)

    # Calculate the slope of the green lane lines
    left_slope = (left_y2 - left_y1) / (left_x2 - left_x1)
    right_slope = (right_y2 - right_y1) / (right_x2 - right_x1)

    # Calculate the y-coordinate for the top corners of the blue lane area
    top_left_y = min(left_y1, left_y2, right_y1, right_y2)  # Use the minimum y-coordinate among the green lane lines
    top_right_y = top_left_y

    # Calculate the x-coordinate for the top corners of the blue lane area
    top_left_x = int((top_left_y - left_y1) / left_slope) + left_x1
    top_right_x = int((top_right_y - right_y1) / right_slope) + right_x1

    # Define the top corners of the blue lane area
    top_left = (top_left_x, top_left_y)
    top_right = (top_right_x, top_right_y)

    

    # Draw blue lane area
    cv.fillPoly(image, np.array([[bottom_left, bottom_right, top_right, top_left]], dtype=np.int32), (255, 0, 0))

    return image

# Read the image
img = cv.imread('road-line.jpeg')

# Detect lanes
result = detect_lanes(img)

# Display the result
cv.imshow('Detected Lanes', result)
cv.waitKey(0)
cv.destroyAllWindows()
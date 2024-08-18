import cv2 as cv
import numpy as np

frame_width, frame_height = 640, 480
cap = cv.VideoCapture(0)
cap.set(3, frame_width)
cap.set(4, frame_height)
cap.set(10, 150)

# HSV values
my_colours = [
    [5, 107, 0, 19, 255, 255], # orange
    [133, 56, 0, 159, 156, 255], # purple
    [57, 76, 0, 100, 255, 255], # green
    [90, 48, 0, 118, 255, 255] # blue
] 

# BGR values
my_colour_values = [
    [51, 153, 255],
    [255, 0, 255],
    [0, 255, 0],
    [255, 0, 0]
]

my_points =  []  # [x, y, colour_ID ]


def findColour(img, my_colours, my_colour_values):
    img_HSV = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    count = 0
    new_points = []
    for colour in my_colours:
        lower = np.array(colour[0:3])
        upper = np.array(colour[3:6])
        mask = cv.inRange(img_HSV, lower, upper)
        x, y = getContours(mask)
        cv.circle(img_result, (x, y), 10, my_colour_values[count], cv.FILLED)
        if x != 0 and y != 0:
            new_points.append([x, y, count])
        count += 1
        # cv.imshow(str(colour[0]), mask)
    return new_points


def getContours(img):
    contours, hierarchy = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv.contourArea(cnt)
        if area > 500:
            # cv.drawContours(img_result, cnt, -1, (255, 0, 0), 3)
            peri = cv.arcLength(cnt, True)
            approx = cv.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv.boundingRect(approx)
    return x + w // 2, y


def drawOnCanvas(my_points, my_colour_values):
    for point in my_points:
        cv.circle(img_result, (point[0], point[1]), 10, my_colour_values[point[2]], cv.FILLED)


while True:
    success, img = cap.read()
    img_result = img.copy()
    new_points = findColour(img, my_colours, my_colour_values)
    if len(new_points) != 0:
        for new_point in new_points:
            my_points.append(new_point)
    if len(my_points) != 0:
        drawOnCanvas(my_points, my_colour_values)
    cv.imshow("Result", img_result)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

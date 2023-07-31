import lane_detection
import matplotlib.pyplot as plt
import cv2
import numpy as np

def get_lane_center(lanes):
    slope1 = (lanes[0][0][3] - lanes[0][0][1])/(lanes[0][0][2] - lanes[0][0][0])
    slope2 = (lanes[0][1][3] - lanes[0][1][1])/(lanes[0][1][2] - lanes[0][1][0])
    center1 = -(lanes[0][0][1] - (lanes[0][0][0]*slope1))/slope1
    center2 = -(lanes[0][1][1] - (lanes[0][1][0]*slope2))/slope2
    closest = ((center1 + center2)/2, (slope1 + slope2)/2)
    for lane in lanes:
        line1, line2 = lane

        x1a, y1a, x2a, y2a = line1
        x1b, y1b, x2b, y2b = line2

        slope1 = (y2a - y1a) / (x2a - x1a)
        slope2 = (y2b - y1b) / (x2b - x1b)

        y_intercept1 = y2a - x2a * slope1
        x_intercept1 = -y_intercept1/slope1

        y_intercept2 = y2b - x2b * slope2
        x_intercept2 = -y_intercept2/slope2
        
        mid_x_intercept = (x_intercept1 + x_intercept2) / 2
        midslope = 1/(((1/slope1) + (1/slope2))/2)

        if np.abs(closest[0]) <= np.abs(mid_x_intercept):
            continue
        
        closest = (mid_x_intercept, midslope)
    
    return closest

def draw_center_lane(img, xPoint1, yPoint1 = 1080, xPoint2 = 0, yPoint2 = 2125):
    cv2.line(img, (int(xPoint1), yPoint1), (int(xPoint2), int(yPoint2)), (255,0,0), 6)
    plt.imshow(img)
    plt.show()
    return img

def recommend_direction(center, slope, totalRes=1300):
    
    halfOfRes = totalRes/2
    if center < halfOfRes + 20 and center > halfOfRes-20:
        print("Go Forward")
        direction = "forward"
    elif center > halfOfRes:# more than halfway
        print("Strafe right")
        direction = "right"
    else:
        print("Strafe left")
        direction = "left"
    
    if slope > 30 or slope < -30:
        print("Forward")
        angle = 0
    elif slope > 0:
        print("Turn Left")
        angle = np.arctan(slope)
    elif slope < 0:
        print("Turn Right")
        angle = np.arctan(slope)
    return direction, angle
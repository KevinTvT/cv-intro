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

        midpoint1 = ((x1a + x1b)/2, (y1a + y1b)/2)
        midpoint2 = ((x2a + x2b)/2, (y2a + y2b)/2)
        
        midslope = (midpoint2[1] - midpoint1[1])/(midpoint2[0] - midpoint1[0])
        mid_y_intercept = midpoint1[1] - midslope * midpoint1[0]
        mid_x_intercept = -mid_y_intercept/midslope

        if np.abs(closest[0]) <= np.abs(mid_x_intercept):
            continue
        
        closest = (mid_x_intercept, midslope)
    
    return closest

def draw_center_lane(img, xPoint1, yPoint1 = 1080, xPoint2 = 0, yPoint2 = 2125):
    cv2.line(img, (int(xPoint1), yPoint1), (int(xPoint2), int(yPoint2)), (0,0,255), 6)
    plt.imshow(img)
    plt.show()
    return img

def recommend_direction(center, slope):
    
    halfOfRes = 1920/2
    if center == halfOfRes:
        direction = "forward"
    elif center > halfOfRes:# more than halfway
        print("Strafe right")
        direction = "right"
    else:
        print("Strafe left")
        direction = "left"
    if 1/slope > 0:
        print("Turn right")
    if 1/slope < 0:
        print("Turn Left")
    return direction
import cv2
import math
import matplotlib.pyplot as plt
from random import randrange

def ret_blur(img):
    blur = cv2.GaussianBlur(img,(5,5),cv2.BORDER_DEFAULT)
    plt.imshow(blur)
    return blur

def ret_gray(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    plt.imshow(gray)
    return gray

 # convert to grayscale
def ret_edges(gray, threshold1=60, threshold2=100, apertureSize=3):
    edges = cv2.Canny(gray, threshold1, threshold2, apertureSize=apertureSize) # detect edges
    plt.imshow(edges)
    return edges

def ret_lines(edges, minLineLength, maxLineGap):
        lines = cv2.HoughLinesP(
                edges,
                1,
                math.pi/360,
                80,
                minLineLength=minLineLength,
                maxLineGap=maxLineGap,
        ) # detect lines
        return lines

def rmvExcessLines(lines):
    """Takes in an list of Lines and removes the lines that are overlapping each other (but its not perfect)
    Input:
        lines: list of lines each line has the shape [1, 4]
    returns
        newLines: list of lines each line has the shape [1, 4]"""
    
    slopes = []
    Y_intercepts = []
    newLines = []

    for i in range(len(lines)):
        x1, y1, x2, y2 = lines[i][0]

        slope = (y2-y1)/(x2-x1)
        slopes.append(slope)

        y_intercept = y1 - (x1*slope)
        Y_intercepts.append(y_intercept)


        y_intercepts = [y for _,y in sorted(zip(slopes,Y_intercepts))]
        slopes.sort()
        closeto = False
        ratioTolerance = 0.95
        
        for j in range(1, len(slopes)):
            ratio = (slopes[j-1]/slope, (y_intercepts[j-1]/y_intercept))
            if ratio[0] > ratioTolerance and ratio[1] > ratioTolerance:
                slopes.remove(slope)
                closeto = True
                break
        if not closeto:
            newLines.append(lines[i])
            #cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            #cv2.putText(img, str(slope), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), cv2.LINE_4)
            closeto = False
    return newLines

def detect_lines(img, threshold1=50, threshold2=150, apertureSize=3, minLineLength=100, maxLineGap=10):
    blur = ret_blur(img)
    gray = ret_gray(blur)
    edges = ret_edges(gray, threshold1, threshold2, apertureSize)
    lines = ret_lines(edges, minLineLength, maxLineGap)
    lineList = rmvExcessLines(lines)
    return lineList


def draw_lines(img, lines, color=(0, 255, 0)):
    for line in lines:
        x1, y1, x2, y2 = line[0]
        slope = (y2-y1)/(x2-x1)
        cv2.line(img, (x1, y1), (x2, y2), color, 2)
        cv2.putText(img, str(slope), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 2, color, cv2.LINE_4)
    plt.imshow(img)
    return img

def get_slopes_intercepts(lines):
    slopes = []
    x_intercepts = []
    for line in lines:
        x1, y1, x2, y2 = line[0]

        slope = (y2-y1)/(x2-x1)
        slopes.append(slope)

        x_intercept = -(y1 - (x1*slope))/slope
        x_intercepts.append(x_intercept)
    return slopes, x_intercepts

def detect_lanes(lines):
    slopeList, xInterceptList = get_slopes_intercepts(lines)
    lanes = []
    #check of the lines intersect on the screen
    if len(slopeList)> 1:
        for i in range(0,len(slopeList)):
            for j in range (i+1,len(slopeList)):
                
                InterceptDist = abs(xInterceptList[i]-xInterceptList[j])
                slopeDiff = abs(1/ slopeList[i]-1 /slopeList[j]) 
                if(InterceptDist > 100 and slopeDiff< 1):
                    lane1 = lines[i][0]
                    lane2 = lines[j][0]
                    addedlanes = [lane1,lane2]
                    lanes.append(addedlanes)
    return lanes

def draw_lanes(img, lanes):
    for lane in lanes:
        color = (randrange(255),randrange(255),randrange(255))
        for i in range(2):
            x1, y1, x2, y2 = lane[i]
            slope = (y2-y1)/(x2-x1)
            cv2.line(img, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
            cv2.putText(img, str(slope), (int(x1), int(y1)), cv2.FONT_HERSHEY_SIMPLEX, 3, color, 6)
    plt.imshow(img)
    return img
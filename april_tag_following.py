import cv2
from pymavlink import mavutil
from dt_apriltags import Detector
import matplotlib.pyplot as plt
import numpy as np
from pid import PID
import sys
import signal

def detect_april_tags(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    cameraMatrix = np.array([ 1060.71, 0, 960, 0, 1060.71, 540, 0, 0, 1]).reshape((3,3))
    camera_params = (cameraMatrix[0,0], cameraMatrix[1,1], cameraMatrix[0,2], cameraMatrix[1,2] )
    at_detector = Detector(families='tag36h11',
                       nthreads=1,
                       quad_decimate=1.0,
                       quad_sigma=0.0,
                       refine_edges=1,
                       decode_sharpening=0.25,
                       debug=0)
    
    tags = at_detector.detect(gray, estimate_tag_pose=True, camera_params=camera_params, tag_size=0.1)

    color_img = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)

    x_errors = [(tag.center[0] - (img.shape[1] / 2)) for tag in tags]
    y_errors = [(tag.center[1] - (img.shape[0] / 2)) for tag in tags]

    for tag in tags:
        for idx in range(len(tag.corners)):
            cv2.line(color_img, tuple(tag.corners[idx - 1, :].astype(int)), tuple(tag.corners[idx, :].astype(int)), (255, 0, 0), 5)

        cv2.putText(color_img, str(tag.tag_id),
                    org=(tag.corners[0, 0].astype(int) + 10, tag.corners[0, 1].astype(int) + 10),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
                    fontScale=0.8,
                    color=(0, 0, 255))
    try:
        x_avg_error = sum(x_errors) / len(x_errors)
        y_avg_error = sum(y_errors) / len(y_errors)

        # Crosshair
        cv2.line(color_img, (int(img.shape[1]/2) - 10, int(img.shape[0]/2)), (int(img.shape[1]/2) + 10, int(img.shape[0]/2)), (0, 0, 255), 5)
        cv2.line(color_img, (int(img.shape[1]/2), int(img.shape[0]/2) - 10), (int(img.shape[1]/2), int(img.shape[0]/2) + 10), (0, 0, 255), 5)

        # AprilTag Crosshair
        cv2.line(color_img, (int(img.shape[1]/2 + x_avg_error) - 10, int(img.shape[0]/2 + y_avg_error)), (int(img.shape[1]/2 + x_avg_error) + 10 , int(img.shape[0]/2 + y_avg_error)), (255, 0, 0), 5)
        cv2.line(color_img, (int(img.shape[1]/2 + x_avg_error), int(img.shape[0]/2 + y_avg_error) - 10), (int(img.shape[1]/2 + x_avg_error), int(img.shape[0]/2 + y_avg_error) + 10), (255, 0, 0), 5)

        # Line2Err
        cv2.line(color_img, (int(img.shape[1]/2), int(img.shape[0] / 2)), (int(img.shape[1]/2 + x_avg_error), int(img.shape[0]/2 + y_avg_error)), (255, 0, 0), 5)

        # print(f"tag translateion: {tag.pose_t}")
        # print(f"tag rotateions: {tag.pose_R}")
        # print(f"x error: {x_avg_error}")
        # print(f"y error: {y_avg_error}")
        
        return color_img, tags, x_avg_error, y_avg_error
    except:
         pass
    # plt.imshow(color_img)
    # plt.show()


def draw_tags(img, tags):
    for tag in tags:
            for idx in range(len(tag.corners)):
                cv2.line(img, tuple(tag.corners[idx - 1, :].astype(int)), tuple(tag.corners[idx, :].astype(int)), (0, 255, 0))

            cv2.putText(img, str(tag.tag_id),
                        org=(tag.corners[0, 0].astype(int) + 10, tag.corners[0, 1].astype(int) + 10),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=3,
                        color=(0, 0, 255))
            print(f"tag translateion: {tag.pose_t}")
            print(f"tag rotateions: {tag.pose_R}")
import cv2
from pymavlink import mavutil
from dt_apriltags import Detector
import matplotlib.pyplot as plt
import numpy as np
from pid import PID
import sys
import signal

def set_rc_channel_pwm(mav, channel_id, pwm=1500):
    """Set RC channel pwm value
    Args:a
        channel_id (TYPE): Channel ID
        pwm (int, optional): Channel pwm value 1100-1900
    """
    if channel_id < 1 or channel_id > 18:
        print("Channel does not exist.")
        return

    # Mavlink 2 supports up to 18 channels:
    # https://mavlink.io/en/messages/common.html#RC_CHANNELS_OVERRIDE
    rc_channel_values = [65535 for _ in range(18)]
    rc_channel_values[channel_id - 1] = pwm
    mav.mav.rc_channels_override_send(
        mav.target_system,  # target_system
        mav.target_component,  # target_component
        *rc_channel_values
    )

def set_rotation_power(mav, power=(0, 0, 0)):
    """Set rotation power
    Args:
        power array of int; optional: Power value -100-100
            First value represents depth
            Second value represents forward backward
            Third value represents Left Right
    """
    if power < -100 or power > 100:
        print("Power value out of range.")
        power = np.clip(power, -100, 100)

    power = int(power)

    set_rc_channel_pwm(mav, 3, power[0]) 
    set_rc_channel_pwm(mav, 5, power[1])
    set_rc_channel_pwm(mav, 6, power[2])

def detect_april_tags(img):
    cameraMatrix = np.array([ 1060.71, 0, 960, 0, 1060.71, 540, 0, 0, 1]).reshape((3,3))
    camera_params = ( cameraMatrix[0,0], cameraMatrix[1,1], cameraMatrix[0,2], cameraMatrix[1,2] )
    at_detector = Detector(families='tag36h11',
                       nthreads=1,
                       quad_decimate=1.0,
                       quad_sigma=0.0,
                       refine_edges=1,
                       decode_sharpening=0.25,
                       debug=0)
    tags = at_detector.detect(img, estimate_tag_pose=True, camera_params=camera_params, tag_size=0.1)
    return tags

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

if __name__ == "__main__":
    main()
# init

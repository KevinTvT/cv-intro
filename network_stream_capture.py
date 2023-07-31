import argparse
import lane_detection
import lane_following
import cv2


def main(ip_address):
    vcap = cv2.VideoCapture(f"rtsp://{ip_address}:8554/rovcam")

    try:
        while True:
            # Obtain the frame
            ret, frame = vcap.read()

            # Check frame was received successfully
            if ret:
                print(" YOU GOT THIS ")
                print(frame.shape)
                # Do something with the frame here
                lines = lane_detection.detect_lines(frame, 20, 50, 3, 100, 15)
                lane_detection.draw_lines(frame.copy(), lines)

                lanes = lane_detection.detect_lanes(lines)
                lane_detection.draw_lanes(frame.copy(), lanes)

                closest_intercept, closest_slope = lane_following.get_lane_center(lanes)
                y_intercept = -closest_slope * closest_intercept
                yPoint = 2125 # completely arbitrary amt just has to be bigger than the height of the window
                xPoint = (yPoint - y_intercept)/closest_slope

                lane_following.draw_center_lane(frame, (1080 - y_intercept)/closest_slope, yPoint1=1080, xPoint2=xPoint, yPoint2=yPoint)
                lane_following.recommend_direction(xPoint, closest_slope)


            else:
                pass

    except KeyboardInterrupt:
        # Close the connection
        vcap.release()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Network Stream Capture")
    parser.add_argument("--ip", type=str, help="IP Address of the Network Stream")
    args = parser.parse_args()

    
    main(args.ip)

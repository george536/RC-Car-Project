
import cv2
import numpy as np
import json
from picamera2 import Picamera2, Preview
from threading import Thread
from .DetectionData import DetectionData
import time

picam2 = Picamera2()
picam2.start()


class CameraLaneDetection(Thread):

    def __init__(self):
        super().__init__()

    def run(self):

        with open('CameraLaneDetection/cameraParameters.json', 'r') as file:
            data = json.load(file)
    

        while True:
            img = picam2.capture_array()
            img = cv2.resize(img, (240,320), interpolation = cv2.INTER_AREA)
            #img = img[240:,:]

            lower = np.array([data['hMin'], data['sMin'], data['vMin']])
            upper = np.array([data['hMax'], data['sMax'], data['vMax']])

            # Create HSV Image and threshold into a range.
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, lower, upper)
            
            contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            # next command removed to enhance computation speed
            #cv2.drawContours(img, contours, -1, (0,255,0), 3)
            
            if len(contours)==0:
                continue

            largest_contour = None
            largest_area = 0
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > largest_area:
                    largest_area = area
                    largest_contour = contour

            cnt = largest_contour
            M = cv2.moments(cnt)
            moment_0 = M['m00']
            
            if moment_0 == 0:
                moment_0 = 1
            cx = int(M['m10'] / moment_0)
            cy = int(M['m01'] / moment_0)

            # next command removed to enhance computation speed
            #cv2.circle(img, (cx, cy), 1, (0, 0, 255), 3)
            #cv2.imshow('image', img)

            # Wait longer to prevent freeze for videos.
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

            middle = (img.shape[1]/2)

            # 400 has found to be about minimum area of the tape that the camera can see
            # chaneg if needed
            if largest_area>400:
                off_value = -((middle-cx)/middle)*100
            else:
                off_value = None

            DetectionData.location = off_value

            DetectionData.img = img

        video_cap.release()
        cv2.destroyAllWindows()
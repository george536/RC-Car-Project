
import cv2
import numpy as np
import json
from picamera2 import Picamera2
from threading import Thread
from .DetectionData import DetectionData

picam2 = Picamera2()
picam2.start()

cv2.namedWindow('image')


class CameraLaneDetection(Thread):

    def __init__(self):
        super().__init__()

    def run(self):

        with open('cameraParameters.json', 'r') as file:
            data = json.load(file)
    
        prev_vals = []
        prev = 0
        counter = 0

        while True:
            img = picam2.capture_array()
            img = img[240:,:]

            # Set minimum and max HSV values to display
            #lower = np.array([30, 44, 202])
            #upper = np.array([57, 171, 255])

            lower = np.array([data['hMin'], data['sMin'], data['vMin']])
            upper = np.array([data['hMax'], data['sMax'], data['vMax']])

            # Create HSV Image and threshold into a range.
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, lower, upper)
            
            contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(img, contours, -1, (0,255,0), 3)
            
            if len(contours)==0:
                continue
            cnt = contours[0]
            M = cv2.moments(cnt)
            moment_0 = M['m00']
            
            if moment_0 == 0:
                moment_0 = 1
            cx = int(M['m10'] / moment_0)
            cy = int(M['m01'] / moment_0)

            cv2.circle(img, (cx, cy), 1, (0, 0, 255), 3)

            cv2.imshow('image', img)
            # Wait longer to prevent freeze for videos.
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

            middle = (img.shape[1]/2)
            off_value = -((middle-cx)/middle)*100

            prev_vals.append(off_value)

            if abs(off_value - prev)<30:
                counter +=1 

            prev = off_value

            if counter>3:
                avg_pos = sum(prev_vals)/len(prev_vals)
                print(avg_pos)
                DetectionData.location = avg_pos
                prev_vals = []

        video_cap.release()
        cv2.destroyAllWindows()

cameraLaneDetection = CameraLaneDetection()
cameraLaneDetection.start()
cameraLaneDetection.join()
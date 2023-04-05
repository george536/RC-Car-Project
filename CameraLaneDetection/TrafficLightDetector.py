import cv2
import numpy as np
from picamera2 import Picamera2, Preview
from threading import Thread
from .DetectionData import DetectionData
import time

class TrafficLightDetector(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            img = DetectionData.img

            try:

                lower_red = np.array([111, 69, 161])
                upper_red = np.array([174, 255, 255])
                lower_yellow = np.array([64, 46, 155])
                upper_yellow = np.array([110, 255, 255])

                hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                hsv_2 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                redMask = cv2.inRange(hsv, lower_red, upper_red)
                yellowMask = cv2.inRange(hsv_2, lower_yellow, upper_yellow)
                
                redContours, hierarchy = cv2.findContours(redMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                if len(redContours)!=0:
                    largest_contour = redContours[0]
                    largest_area = 0
                    for contour in redContours:
                        area = cv2.contourArea(contour)
                        if area > largest_area:
                            largest_area = area
                            largest_contour = contour
                    if largest_area>400:
                        DetectionData.currentlyAt['red'] = True
                    else:
                        DetectionData.currentlyAt['red'] = False


                yellowContours, hierarchy = cv2.findContours(yellowMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                if len(yellowContours)!=0:
                    largest_contour = yellowContours[0]
                    largest_area = 0
                    for contour in yellowContours:
                        area = cv2.contourArea(contour)
                        if area > largest_area:
                            largest_area = area
                            largest_contour = contour
                    if largest_area>400:
                        DetectionData.currentlyAt['yellow'] = True
                    else:
                        DetectionData.currentlyAt['yellow'] = False


            except:
                continue
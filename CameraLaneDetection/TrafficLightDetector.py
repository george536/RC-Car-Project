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
                lower_yellow = np.array([64, 98, 132])
                upper_yellow = np.array([110, 255, 255])

                hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                redMask = cv2.inRange(hsv, lower_red, upper_red)
                yellowMask = cv2.inRange(hsv, lower_yellow, upper_yellow)
                
                redContours, hierarchy = cv2.findContours(redMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                yellowContours, hierarchy = cv2.findContours(yellowMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                if len(redContours)!=0:
                    print("red detected")

                if len(yellowContours)!=0:
                    print("yellow detected")
                    
            except:
                continue
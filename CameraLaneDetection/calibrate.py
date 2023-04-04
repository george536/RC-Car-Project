import cv2
import numpy as np
import json
from picamera2 import Picamera2

picam2 = Picamera2()
picam2.start()

def nothing(input):pass

cv2.namedWindow('image')

# # create trackbars for color change
cv2.createTrackbar('HMin','image',0,179,nothing) # Hue is from 0-179 for Opencv
cv2.createTrackbar('SMin','image',0,255,nothing)
cv2.createTrackbar('VMin','image',0,255,nothing)
cv2.createTrackbar('HMax','image',0,179,nothing)
cv2.createTrackbar('SMax','image',0,255,nothing)
cv2.createTrackbar('VMax','image',0,255,nothing)

with open('CameraLaneDetection/cameraParameters.json', 'r') as file:
    data = json.load(file)

# Set default value trackbars.
cv2.setTrackbarPos('HMin', 'image', data['hMin'])
cv2.setTrackbarPos('SMin', 'image', data['sMin'])
cv2.setTrackbarPos('VMin', 'image', data['vMin'])
cv2.setTrackbarPos('HMax', 'image', data['hMax'])
cv2.setTrackbarPos('SMax', 'image', data['sMax'])
cv2.setTrackbarPos('VMax', 'image', data['vMax'])


# Initialize to check if HSV min/max value changes
hMin ,sMin , vMin = data['hMin'], data['sMin'], data['vMin']
hMax , sMax , vMax = data['hMax'], data['sMax'], data['vMax']
phMin = psMin = pvMin = phMax = psMax = pvMax = 0

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    with open('CameraLaneDetection/cameraParameters.json', 'r') as file:
        data = json.load(file)

    while True:
        img = picam2.capture_array()
        img = img[240:,:]

        # # get current positions of all trackbars
        hMin = cv2.getTrackbarPos('HMin', 'image')
        sMin = cv2.getTrackbarPos('SMin', 'image')
        vMin = cv2.getTrackbarPos('VMin', 'image')

        hMax = cv2.getTrackbarPos('HMax', 'image')
        sMax = cv2.getTrackbarPos('SMax', 'image')
        vMax = cv2.getTrackbarPos('VMax', 'image')

        # Set minimum and max HSV values to display
        lower = np.array([hMin, sMin, vMin])
        upper = np.array([hMax, sMax, vMax])

        data['hMin'] = hMin
        data['sMin'] = sMin
        data['vMin'] = vMin
        data['hMax'] = hMax
        data['sMax'] = sMax
        data['vMax'] = vMax

        with open('CameraLaneDetection/cameraParameters.json', 'w') as file:
            json.dump(data, file)
        

        # Create HSV Image and threshold into a range.
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(img, contours, -1, (0,255,0), 3)
        
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

        cv2.circle(img, (cx, cy), 1, (0, 0, 255), 3)

        cv2.imshow('image', img)
        # Wait longer to prevent freeze for videos.
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    video_cap.release()
    cv2.destroyAllWindows()

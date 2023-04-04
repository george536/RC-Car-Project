import tkinter as tk
from .DetectionData import DetectionData
import json

def updateKI(ki):

    ki = float(ki)

    with open('CameraLaneDetection/PIDparameters.json', 'w') as file:
        global data
        data['ki'] = ki 
        json.dump(data, file)

    DetectionData.ki = ki 

def updateKd(kd):

    kd = float(kd)

    with open('CameraLaneDetection/PIDparameters.json', 'w') as file:
        global data
        data['kd'] = kd 
        json.dump(data, file)

    DetectionData.kd = kd

def updateKp(kp): 

    kp = float(kp)

    with open('CameraLaneDetection/PIDparameters.json', 'w') as file:
        global data
        data['kp'] = kp 
        json.dump(data, file)

    DetectionData.kp = kp

def updateSpeed(testSpeed): 
    DetectionData.testSpeed = float(testSpeed)

class SliderInterface:
    def __init__(self):
        master = tk.Tk()
        master.title("Slider Interface")

        with open('CameraLaneDetection/PIDparameters.json', 'r') as file:
            global data
            data = json.load(file)

        # # Initialize variables
        self.kp = tk.DoubleVar()
        self.ki = tk.DoubleVar()
        self.kd = tk.DoubleVar()
        self.testSpeed = tk.DoubleVar()

        # Create sliders
        self.slider1 = tk.Scale(master, from_=0, to=50, length=1000, resolution=0.01, variable=self.kp, label="kp", command = updateKp, orient="horizontal")
        self.slider1.set(data['kp'])
        self.slider2 = tk.Scale(master, from_=0, to=5, length=1000, resolution=0.00001, variable=self.ki, label="ki", command = updateKI, orient="horizontal")
        self.slider2.set(data['ki'])
        self.slider3 = tk.Scale(master, from_=0, to=5, length=1000, resolution=0.00001, variable=self.kd, label="kd", command = updateKd, orient="horizontal")
        self.slider3.set(data['kd'])
        self.slider4 = tk.Scale(master, from_=0, to=120, length=1000, resolution=1, variable=self.testSpeed, label="speed", command = updateSpeed, orient="horizontal")
        self.slider4.set(DetectionData.kd)

        # Pack sliders into the window
        self.slider1.pack()
        self.slider2.pack()
        self.slider3.pack()
        self.slider4.pack()


        master.mainloop() 




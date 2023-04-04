import tkinter as tk
from .DetectionData import DetectionData

def updateKI(ki):
    DetectionData.ki = float(ki)
def updateKd(kd):
    DetectionData.kd = float(kd)
def updateKp(kp): 
    DetectionData.kp = float(kp)
def updateSpeed(testSpeed): 
    DetectionData.testSpeed = float(testSpeed)

class SliderInterface:
    def __init__(self):
        master = tk.Tk()
        master.title("Slider Interface")

        # # Initialize variables
        self.kp = tk.DoubleVar()
        self.ki = tk.DoubleVar()
        self.kd = tk.DoubleVar()
        self.testSpeed = tk.DoubleVar()

        # Create sliders
        self.slider1 = tk.Scale(master, from_=0, to=50, length=1000, resolution=0.01, variable=self.kp, label="kp", command = updateKp, orient="horizontal")
        self.slider1.set(DetectionData.kp)
        self.slider2 = tk.Scale(master, from_=0, to=5, length=1000, resolution=0.00001, variable=self.ki, label="ki", command = updateKI, orient="horizontal")
        self.slider2.set(DetectionData.ki)
        self.slider3 = tk.Scale(master, from_=0, to=5, length=1000, resolution=0.00001, variable=self.kd, label="kd", command = updateKd, orient="horizontal")
        self.slider3.set(DetectionData.kd)
        self.slider4 = tk.Scale(master, from_=0, to=120, length=1000, resolution=1, variable=self.testSpeed, label="speed", command = updateSpeed, orient="horizontal")
        self.slider4.set(DetectionData.kd)

        # Pack sliders into the window
        self.slider1.pack()
        self.slider2.pack()
        self.slider3.pack()
        self.slider4.pack()


        master.mainloop() 




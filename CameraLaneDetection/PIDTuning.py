import tkinter as tk
from .DetectionData import DetectionData

def updateKI(ki):
    DetectionData.ki = ki
def updateKd(kd):
    DetectionData.kd = kd
def updateKp(kp): 
    DetectionData.kp = kp

class SliderInterface:
    def __init__(self, master):
        self.master = master
        master.title("Slider Interface")

        # Initialize variables
        self.kp = tk.DoubleVar()
        self.ki = tk.DoubleVar()
        self.kd = tk.DoubleVar()

        # Create sliders
        self.slider1 = tk.Scale(master, from_=0, to=1, resolution=0.01, variable=DetectionData.kp, label="kp", commmand = updateKp)
        self.slider1.set(DetectionData.kp)
        self.slider2 = tk.Scale(master, from_=0, to=1, resolution=0.01, variable=DetectionData.ki, label="ki", commmand = updateKI)
        self.slider2.set(DetectionData.ki)
        self.slider3 = tk.Scale(master, from_=0, to=1, resolution=0.01, variable=DetectionData.kd, label="kd", commmand = updateKd)
        self.slider3.set(DetectionData.kd)

        # Pack sliders into the window
        self.slider1.pack()
        self.slider2.pack()
        self.slider3.pack()


        self.master.mainloop() 




import tkinter as tk
from .DetectionData import DetectionData

def updateKI(ki):
    DetectionData.ki = float(ki)
def updateKd(kd):
    DetectionData.kd = float(kd)
def updateKp(kp): 
    DetectionData.kp = float(kp)

class SliderInterface:
    def __init__(self, master):
        self.master = master
        master.title("Slider Interface")

        # # Initialize variables
        self.kp = tk.DoubleVar()
        self.ki = tk.DoubleVar()
        self.kd = tk.DoubleVar()

        # Create sliders
        self.slider1 = tk.Scale(master, from_=0, to=25, resolution=0.01, variable=self.kp, label="kp", command = updateKp)
        self.slider1.set(DetectionData.kp)
        self.slider2 = tk.Scale(master, from_=0, to=1, resolution=0.0001, variable=self.ki, label="ki", command = updateKI)
        self.slider2.set(DetectionData.ki)
        self.slider3 = tk.Scale(master, from_=0, to=1, resolution=0.0001, variable=self.kd, label="kd", command = updateKd)
        self.slider3.set(DetectionData.kd)

        # Pack sliders into the window
        self.slider1.pack()
        self.slider2.pack()
        self.slider3.pack()


        self.master.mainloop() 




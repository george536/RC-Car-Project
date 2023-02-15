import time
from PathTracking.Positions import Position
from .Motor import *
import RPi.GPIO as GPIO

class Line_Tracking:
    def __init__(self):
        self.IR01 = 14
        self.IR02 = 15
        self.IR03 = 23
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.IR01,GPIO.IN)
        GPIO.setup(self.IR02,GPIO.IN)
        GPIO.setup(self.IR03,GPIO.IN)
        
    
    def run(self,speed):

        boundry1 = speed * 1.5
        if boundry1>4096:
            boundry1 = 4096

        boundry1 = int(boundry1)

        boundry2 = speed * 2.5
        if boundry2>4096:
            boundry2 = 4096

        boundry2 = int(boundry2)

        self.LMR=0x00
        if GPIO.input(self.IR01)==True:
            self.LMR=(self.LMR | 4)
        if GPIO.input(self.IR02)==True:
            self.LMR=(self.LMR | 2)
        if GPIO.input(self.IR03)==True:
            self.LMR=(self.LMR | 1)
            
        if self.LMR==Position.Middle.value:
            PWM.setMotorModel(-speed,-speed,-speed,-speed)
        elif self.LMR==Position.Left.value:
            PWM.setMotorModel(boundry1,boundry1,-boundry2,-boundry2)
        elif self.LMR==Position.Right.value:
            PWM.setMotorModel(-boundry2,-boundry2,boundry1,boundry1)
        elif self.LMR==6:
            PWM.setMotorModel(2000,2000,-4000,-4000)
        elif self.LMR==3:
            PWM.setMotorModel(-4000,-4000,2000,2000)
        else:
            PWM.setMotorModel(0,0,0,0)
            PWM.setMotorModel(0,0,0,0)
            PWM.setMotorModel(0,0,0,0)
            PWM.setMotorModel(0,0,0,0)


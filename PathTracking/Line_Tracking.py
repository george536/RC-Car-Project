import time
from Positions import Position
from Motor import *
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
        
    def getPosition(self):
        for position in list(Position):
            if self.LMR == position.value:
                return position
                
        return position.Failed
    
    def test(self):
        print("test")
    
    def run(self):
        while True:
            self.LMR=0x00
            if GPIO.input(self.IR01)==True:
                self.LMR=(self.LMR | 4)
            if GPIO.input(self.IR02)==True:
                self.LMR=(self.LMR | 2)
            if GPIO.input(self.IR03)==True:
                self.LMR=(self.LMR | 1)
            if self.LMR==2:
                print(self.LMR)
                #PWM.setMotorModel(800,800,800,800)
            elif self.LMR==4:
                print(self.LMR)
                #PWM.setMotorModel(-1500,-1500,2500,2500)
            elif self.LMR==6:
                print(self.LMR)
                #PWM.setMotorModel(-2000,-2000,4000,4000)
            elif self.LMR==1:
                print(self.LMR)
                #PWM.setMotorModel(2500,2500,-1500,-1500)
            elif self.LMR==3:
                print(self.LMR)
                #PWM.setMotorModel(4000,4000,-2000,-2000)
            elif self.LMR==7:
                print(self.LMR)
                #pass
                #PWM.setMotorModel(0,0,0,0)

                
#infrared=Line_Tracking()
# Main program logic follows:
#if __name__ == '__main__':
#    print ('Program is starting ... ')
 #   try:
  #      #infrared.run()
   #     pass
    #except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program  will be  executed.
     #   PWM.setMotorModel(0,0,0,0)

from .DetectionData import DetectionData
from RcCarModules.Motor import *
import HelperFunctions.SpeedScale
import time
import math

class CamLaneTracking:
    def __init__(self,ultrasonicManager,egoCar):
        self.ultrasonicManager = ultrasonicManager
        self.egoCar = egoCar

        # PID values
        self.kp = int(DetectionData.kp)
        self.ki = int(DetectionData.ki)
        self.kd = int(DetectionData.kd)

        self.error = 0
        self.integral = 0
        self.previous_error = 0
        self.last_time = time.time()

    def update(self):
            self.kp = int(DetectionData.kp)
            self.ki = int(DetectionData.ki)
            self.kd = int(DetectionData.kd)

            self.error = DetectionData.location
            origionalError = self.error


            if self.error == None:
                self.egoCar.setSpeed(0)
                self.ultrasonicManager.emergencyStop = True
                PWM.setMotorModel(0,0,0,0)
                return
            else:
                self.ultrasonicManager.emergencyStop = False
    
            self.error = abs(self.error)

            speed = self.egoCar.getScaledSpeed()

            if DetectionData.testSpeed != None:
                speed = SpeedScale.scaleToRC(DetectionData.testSpeed)
            
            t = time.time()
            dt = t-self.last_time

            proportional =  self.kp * self.error
            self.integral += self.error * dt
            derivative =  self.kd * ( self.error -  self.previous_error) / dt

            integral = (self.integral * self.ki)

            if math.isnan(integral):
                integral = 0

            if integral!=0:
                integral = min(integral, 2000)
                integral = max(integral, -2000)

            output = proportional + integral + derivative

            self.previous_error = self.error

            output = int(output)

            if self.ultrasonicManager.getEmergencyStopState()==False :
                
                speed_in_km = self.egoCar.getSpeed()

                if int(speed_in_km) ==0:
                    PWM.setMotorModel(0,0,0,0)
                    return

                fixValue = -speed+output
                if (fixValue)>0:
                    fixValue = 0

                if origionalError > 0:
                    PWM.setMotorModel(-speed,-speed,fixValue,fixValue)
                else:
                    PWM.setMotorModel(fixValue,fixValue,-speed,-speed)
                    
            else:
                self.egoCar.setSpeed(0)

            # time.sleep(0.005)

            self.last_time = time.time()
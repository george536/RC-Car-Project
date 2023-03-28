from .DetectionData import DetectionData
from RcCarModules.Motor import *
import time
import math

class CamLaneTracking:
    def __init__(self,ultrasonicManager,egoCar):
        self.ultrasonicManager = ultrasonicManager
        self.egoCar = egoCar

        # PID values
        # good was 22
        self.kp = int(DetectionData.kp)
        self.ki = int(DetectionData.ki)
        # origionally 0.001
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

            if self.error == None:
                PWM.setMotorModel(0,0,0,0)
                return

            if abs(self.error) > 35:
                self.kp = 40
                self.ki = 0
                self.kd = 0
            
            t = time.time()
            dt = t-self.last_time

            proportional =  self.kp * self.error
            self.integral += self.error * dt
            derivative =  self.kd * ( self.error -  self.previous_error) / dt

            #  (self.integral * self.ki) causing NaN
            integral = (self.integral * self.ki)

            if math.isnan(integral):
                integral = 0

            if integral!=0:
                integral = max(integral, 2000)
                integral = min(integral, -2000)

            output = proportional - integral - derivative

            self.previous_error = self.error

            #print("Output by PId: "+str(output))

            output = int(output)

            if self.ultrasonicManager.getEmergencyStopState()==False :
                speed = self.egoCar.getScaledSpeed()
                speed_in_km = self.egoCar.getSpeed()

                if int(speed_in_km) ==0:
                    PWM.setMotorModel(0,0,0,0)
                    return

                # if speed_in_km > 40:
                #     self.kp = 18
                # else:
                #     self.kp = 22

                # speed reduction on curves
                # if self.error >40 and self.egoCar.getSpeed()>70:
                #     speed = int(speed * 0.8)

                if self.error > 0:
                    PWM.setMotorModel(-speed,-speed,-speed+output,-speed+output)
                else:
                    PWM.setMotorModel(-speed+output,-speed+output,-speed,-speed)
                    
            else:
                pass
                #self.egoCar.setSpeed(0)

            #time.sleep(0.005)

            self.last_time = time.time()
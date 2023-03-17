from .DetectionData import DetectionData
from RcCarModules.Motor import *
import time
import math

class CamLaneTracking:
    def __init__(self,ultrasonicManager,egoCar):
        self.ultrasonicManager = ultrasonicManager
        self.egoCar = egoCar
        self.safeZone = 30

        # PID values
        # good was 20
        self.kp =21
        self.ki = 0
        self.kd = 0.001

        self.error = 0
        self.integral = 0
        self.previous_error = 0
        self.last_time = time.time()

    def update(self):

            self.error = DetectionData.location

            if math.isnan(self.error):
                print("Error is NAN")

            t = time.time()
            dt = t-self.last_time

            proportional =  self.kp * self.error
            self.integral += min(4096, self.integral + self.error * dt)
            derivative =  self.kd * ( self.error -  self.previous_error) / dt

            if math.isnan(derivative):
                derivative = 0

            output = proportional + (self.integral * self.ki) + derivative

            self.previous_error = self.error

            #print("Output by PId: "+str(output))

            if math.isnan(proportional):
                print("proportional is NAN")

            if math.isnan(output):
                return
                print("Output is NAN")
                output = 0


            output = int(output)

            if self.ultrasonicManager.getEmergencyStopState()==False :
                speed = self.egoCar.getScaledSpeed()
                speed_in_km = self.egoCar.getSpeed()
                if speed_in_km ==0:
                    return
                # speed reduction on curves
                if self.error >40 and self.egoCar.getSpeed()>70:
                    speed = int(speed * 0.8)
                if self.error > 0:
                    PWM.setMotorModel(-speed,-speed,-speed+output,-speed+output)
                else:
                    PWM.setMotorModel(-speed-output,-speed-output,-speed,-speed)
            else:
                pass
                #self.egoCar.setSpeed(0)

            time.sleep(0.01)

            self.last_time = time.time()
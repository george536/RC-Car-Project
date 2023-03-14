from .DetectionData import DetectionData
from RcCarModules.Motor import *
import time

class CamLaneTracking:
    def __init__(self,ultrasonicManager,egoCar):
        self.ultrasonicManager = ultrasonicManager
        self.egoCar = egoCar
        self.safeZone = 10

        # PID values
        # good was 17
        self.kp =16.5
        self.ki = 0
        self.kd = 0

        self.error = 0
        self.integral = 0
        self.previous_error = 0
        self.last_time = time.time()

    def update(self):

            self.error = DetectionData.location

            t = time.time()
            dt = t-self.last_time

            proportional =  self.kp * self.error
            self.integral += min(4096, self.integral + self.error * dt)
            derivative =  self.kd * ( self.error -  self.previous_error) / dt

            output = proportional + (self.integral * self.ki) + derivative

            self.previous_error = self.error

            print("Output by PId: "+str(output))


            output = int(output)

            if self.ultrasonicManager.getEmergencyStopState()==False:
                speed = self.egoCar.getScaledSpeed()
                #if abs(DetectionData.location)<self.safeZone:
                #    pass
                    #PWM.setMotorModel(-speed,-speed,-speed,-speed)

                if self.error > 0:
                    PWM.setMotorModel(-speed,-speed,-speed+output,-speed+output)
                else:
                    PWM.setMotorModel(-speed-output,-speed-output,-speed,-speed)
            else:
                pass
                #self.egoCar.setSpeed(0)

            time.sleep(0.01)

            self.last_time = time.time()
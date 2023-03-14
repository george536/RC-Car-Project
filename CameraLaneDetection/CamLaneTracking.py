from .DetectionData import DetectionData
from RcCarModules.Motor import *

class CamLaneTracking:
    def __init__(self,ultrasonicManager,egoCar):
        self.ultrasonicManager = ultrasonicManager
        self.egoCar = egoCar
        self.safeZone = 10

        # PID values
        self.kp = 2
        self.ki = 1
        self.kd = 2

        self.error = 0
        self.integral = 0
        self.previous_error = 0
		
    def update(self):

            position = DetectionData.location
            self.error = position -0.5

            target_speed = 50 + (1 - abs(self.error)) * 50

            current_speed = self.egoCar.getScaledSpeed()

            feedback = current_speed - target_speed

            proportional =  self.kp * self.error
            self.integral += self.ki * (self.error + feedback)
            derivative =  self.kd * ( self.error -  self.previous_error)

            output = proportional + self.integral + derivative

            self.previous_error = self.error

            print("Error by PId: "+str(self.error))

            self.error = int(self.error)

            if self.ultrasonicManager.getEmergencyStopState()==False:
                speed = self.egoCar.getScaledSpeed()
                #if abs(DetectionData.location)<self.safeZone:
                #    pass
                    #PWM.setMotorModel(-speed,-speed,-speed,-speed)
                if self.error > 0:
                    PWM.setMotorModel(-speed,-speed,-speed+self.error,-speed+self.error)
                else:
                    PWM.setMotorModel(-speed+self.error,-speed+self.error,-speed,-speed)
            else:
                pass
                #self.egoCar.setSpeed(0)

            time.sleep(0.01)
from .DetectionData import DetectionData
from RcCarModules.Motor import *

class CamLaneTracking:
    def __init__(self,ultrasonicManager,egoCar):
        self.ultrasonicManager = ultrasonicManager
        self.egoCar = egoCar
        self.safeZone = 10

        # PID values
        self.kp = 0.5
        self.ki = 0.1
        self.kd = 0.2

        self.error = 0
        self.integral = 0
        self.previous_error = 0

        self.rightVal = 0
        self.leftVal = 0
		
    def update(self):

            self.error = DetectionData.location

            current_speed = self.egoCar.getScaledSpeed()

            target_speed = current_speed + (1 - abs(self.error)) * current_speed

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
                    self.leftVal=0
                    self.rightVal += self.error
                    PWM.setMotorModel(-speed,-speed,-speed+self.rightVal,-speed+self.rightVal)
                else:
                    self.rightVal=0
                    self.leftVal += self.error
                    PWM.setMotorModel(-speed-self.leftVal,-speed-self.leftVal,-speed,-speed)
            else:
                pass
                #self.egoCar.setSpeed(0)

            time.sleep(0.01)
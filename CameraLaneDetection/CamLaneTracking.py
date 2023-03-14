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
		
    def update(self):

            self.error = DetectionData.location

            proportional =  self.kp * self.error
            integral += self.ki * self.error
            derivative =  self.kd * ( self.error -  self.previous_error)

            output = proportional + integral + derivative

            self.previous_error = self.error

            print("Error by PId: "+str(self.error))

            if self.ultrasonicManager.getEmergencyStopState()==False:
                speed = self.egoCar.getScaledSpeed()
                if abs(DetectionData.location)<self.safeZone:
                    pass
                    #PWM.setMotorModel(-speed,-speed,-speed,-speed)
            else:
                self.egoCar.setSpeed(0)

            time.sleep(0.01)
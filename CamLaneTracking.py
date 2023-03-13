from .DetectionData import DetectionData
from .RcCarModules.Motor import *

class CamLaneTracking:
    def __init__(self,ultrasonicManager,egoCar):
        self.ultrasonicManager = ultrasonicManager
        self.egoCar = egoCar
        self.safeZone = 10
		
    def update(self):

            if self.ultrasonicManager.getEmergencyStopState()==False:
                speed = self.egoCar.getScaledSpeed()
                if abs(DetectionData.location)<self.safeZone:
                    PWM.setMotorModel(-speed,-speed,-speed,-speed)
            else:
                self.egoCar.setSpeed(0)
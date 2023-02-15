from CarControls.CarCommands import CarCommands
from UltrasonicActions.CollisionDetection import CollisionDetection 
from UltrasonicActions.LeadCarDetection import LeadCarDetection 
from UltrasonicActions.ObserverManager import ObserverManager as UltrasonicManager
from PathTracking.LaneCentering import LaneCentering
from PathTracking.ObserverManager import ObserverManager as PathManager
import HelperFunctions.SpeedScale as speedScale
from threading import Thread
import time
import sys
import os
from RcCarModules.Motor import *


# driving scenario thread
class DrivingScenario(Thread):
	def __init__(self,ultrasonicManager):
		super().__init__()
		# ultrasonicManager manager is the observer that checks for emergency stops
		self.ctrl = CarCommands(ultrasonicManager)
		
	def run(self):
            #while True:
            self.ctrl.DriveForward(500)
		
class detectCollision(Thread):
	def __init__(self,ultrasonicManager):
		super().__init__()
		
		self.observerManager = ultrasonicManager
		CollisionDetection(self.observerManager)
		LeadCarDetection(self.observerManager)
		
	def run(self):
	
		while True:
			self.observerManager.notifyAllObservers()


class TrackingPath(Thread):
	def __init__(self,observerManager,ultrasonicManager,egoCar):
		super().__init__()

		self.observerManager = observerManager
		LaneCentering(self.observerManager,ultrasonicManager,egoCar)

	def run(self):
		while True:
			self.observerManager.notifyAllObservers()

# to be replaced
class car:
	def __init__(self):
		self.speed = speedScale.scaleToRC(100)

	def getSpeed(self):
		return self.speed
		
def main():
    threads = []
    ultrasonicManager = UltrasonicManager()
    pathManager = PathManager()
    egoCar = car()

    #threads.append(DrivingScenario(ultrasonicManager))
    threads.append(detectCollision(ultrasonicManager))
    threads.append(TrackingPath(pathManager,ultrasonicManager,egoCar))


    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


try: 
    main()
except Exception as e:
    print(e)
    PWM.setMotorModel(0,0,0,0)
    PWM.setMotorModel(0,0,0,0)
    PWM.setMotorModel(0,0,0,0)
    PWM.setMotorModel(0,0,0,0)

    try:
        sys.exit(130)
    except SystemExit:
        os._exit(130)













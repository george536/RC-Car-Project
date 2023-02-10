from CarControls.CarCommands import CarCommands
from UltrasonicActions.CollisionDetection import CollisionDetection 
from UltrasonicActions.ObserverManager import ObserverManager as UltrasonicManager
from PathTracking.LaneCentering import LaneCentering
from PathTracking.ObserverManager import ObserverManager as PathManager
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
		#self.ctrl.changeSpeed(500,2000,50,0.1)
		#self.ctrl.changeSpeed(2000,500,50,0.1)
		#self.ctrl.changeSpeed(500,2000,100,0.1)
		#self.ctrl.turn(90)
		#self.ctrl.changeSpeed(2000,500,100,0.1)
            while True:
                
                self.ctrl.DriveForward(500)

		#self.ctrl.stop()
		
class detectCollision(Thread):
	def __init__(self,ultrasonicManager):
		super().__init__()
		
		self.observerManager = ultrasonicManager
		CollisionDetection(self.observerManager)
		
	def run(self):
	
		while True:
			self.observerManager.notifyAllObservers()


class TrackingPath(Thread):
	def __init__(self,observerManager,ultrasonicManager):
		super().__init__()

		self.observerManager = observerManager
		LaneCentering(self.observerManager,ultrasonicManager)

	def run(self):
		while True:
			self.observerManager.notifyAllObservers()
		
def main():
    threads = []
    ultrasonicManager = UltrasonicManager()
    pathManager = PathManager()

    #threads.append(DrivingScenario(ultrasonicManager))
    threads.append(detectCollision(ultrasonicManager))
    threads.append(TrackingPath(pathManager,ultrasonicManager))


    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


try: 
    main()
except:
    PWM.setMotorModel(0,0,0,0)
    PWM.setMotorModel(0,0,0,0)
    PWM.setMotorModel(0,0,0,0)
    PWM.setMotorModel(0,0,0,0)
    try:
        sys.exit(130)
    except SystemExit:
        os._exit(130)













from CarControls.CarCommands import CarCommands
from UltrasonicActions.CollisionDetection import CollisionDetection 
from UltrasonicActions.ObserverManager import ObserverManager 
from threading import Thread
import time
class DrivingScenario(Thread):
	def __init__(self,collisionObserver):
		super().__init__()
		self.ctrl = CarCommands(collisionObserver)
		
	def run(self):
		#self.ctrl.changeSpeed(500,2000,50,0.1)
		#self.ctrl.changeSpeed(2000,500,50,0.1)
		#self.ctrl.changeSpeed(500,2000,100,0.1)
		#self.ctrl.turn(90)
		#self.ctrl.changeSpeed(2000,500,100,0.1)
		while True:
			self.ctrl.DriveForward(3000)
		#self.ctrl.stop()
		
class detectCollision(Thread):
	def __init__(self,observerManager):
		super().__init__()
		
		self.observerManager = observerManager
		CollisionDetection(self.observerManager)
		
	def run(self):
	
		while True:
			self.observerManager.notifyAllObservers()
			
threads = []
observerManager = ObserverManager()
threads.append(DrivingScenario(observerManager))
threads.append(detectCollision(observerManager))


for thread in threads:
	thread.start()

for thread in threads:
	thread.join()














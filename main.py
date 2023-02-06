from CarControls.CarCommands import CarCommands
from UltrasonicActions.CollisionDetection import CollisionDetection 
from UltrasonicActions.ObserverManager import ObserverManager 
from threading import Thread

class DrivingScenario(Thread):
	def __init__(self,collisionObserver):
		super().__init__()
		self.ctrl = CarCommands(collisionObserver)
		
	def run(self):
		self.ctrl.accelerate(500,1000,50,0.1)
		self.ctrl.decelerate(1000,500,50,0.1)
		self.ctrl.stop()
		
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














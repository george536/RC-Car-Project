from .UltrasonicObserver import *

class CollisionDetection(UltrasonicObserver):
	
	def __init__(self,observerManager):
		super().__init__()
		self.observerManager = observerManager
		observerManager.attach(self)
		self.minimum = 10 # default minimum distance
		
	def update(self):
		if ultrasonic.get_distance() <=self.minimum:
		    
		    self.observerManager.emergencyStop = True
		    PWM.setMotorModel(0,0,0,0)
		else:
		    self.observerManager.emergencyStop = False  

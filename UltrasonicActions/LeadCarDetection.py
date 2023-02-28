from .UltrasonicObserver import *
import time


# This is on hold for now

class LeadCarDetection(UltrasonicObserver):
	
	def __init__(self,observerManager):
		super().__init__()
		self.observerManager = observerManager
		observerManager.attach(self)
		self.likelyhood = 0
		self.maxDistance = 4*20 # default minimum distance
		self.last_d = 0
		self.last_t = time.time()
		self.lastSpeed = 0
		
	def update(self):
		if ultrasonic.get_distance() <=self.maxDistance:
            
		    d= ultrasonic.get_distance()
		    t = time.time()

		    speed = 3.6*(10**-2)*(d-self.last_d)*22.5/(t-self.last_t)
		    speed=int(speed)
		    self.last_d=d
		    self.last_t=t

		    print(speed)

		    self.lastSpeed = speed


		    
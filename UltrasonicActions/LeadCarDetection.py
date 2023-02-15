from .UltrasonicObserver import *
import time

class LeadCarDetection(UltrasonicObserver):
	
	def __init__(self,observerManager):
		super().__init__()
		self.observerManager = observerManager
		observerManager.attach(self)
		self.likelyhood = 0
		self.minimum = 50 # default minimum distance
        self.last_d = 0
        self.last_t = 0
		
	def update(self):
		if ultrasonic.get_distance() <=self.minimum:
            d= ultrasonic.get_distance()
            t = time.time()

            speed = (d-self.last_d)/(t-self.last_t)

            self.last_d=d
            self.last_t=t

            print(speed)

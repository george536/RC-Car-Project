from .UltrasonicObserver import *
from MQTT.CarInfo import CarInfo
from MQTT.topics import Topic
from RcCarModules.led import Led
from rpi_ws281x import *

class CollisionDetection(UltrasonicObserver):
	
	def __init__(self,observerManager):
		super().__init__()
		self.observerManager = observerManager
		observerManager.attach(self)
		self.likelyhood = 0
		self.minimum = 15 # default minimum distance in cm
		self.led = Led()
		
	def update(self):
		if ultrasonic.get_distance() <=self.minimum:
		    self.likelyhood += 1
		    if self.likelyhood >=3:
			    self.likelyhood = 0
			    self.observerManager.emergencyStop = True
			    PWM.setMotorModel(0,0,0,0)
			    self.led.colorWipe(self.led.strip, Color(255, 0, 0))
			    print("Emergency Stop "+str(ultrasonic.get_distance()))
		else:
			if self.observerManager.emergencyStop == True:
			    self.observerManager.emergencyStop = False  
				self.led.colorWipe(self.led.strip, Color(0,0,0),10)

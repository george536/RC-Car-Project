from .UltrasonicObserver import *
from MQTT.CarInfo import CarInfo
from MQTT.topics import Topic
from RcCarModules.led import Led
from rpi_ws281x import *
from CarControls.CarCommands import CarCommands

class CollisionDetection(UltrasonicObserver):
	
	def __init__(self,observerManager, stoppingDistance, likelihoodBound):
		super().__init__()
		self.observerManager = observerManager
		observerManager.attach(self)
		self.likelihood = 0
		self.minimum = stoppingDistance # distance in cm
		self.led = Led()
		self.likelihoodBound = likelihoodBound
		self.carCommands = CarCommands(observerManager)
		
	def update(self):
		if ultrasonic.get_distance() <=self.minimum:
			# the likelihood is used because the sensor has lot of noise
			self.likelihood += 1

			if self.likelihood >= self.likelihoodBound:

				self.likelihood = 0
				self.observerManager.emergencyStop = True
				self.carCommands.stop()
				self.led.colorWipe(self.led.strip, Color(100, 0, 0))

		else:
			if self.observerManager.emergencyStop == True:
				self.observerManager.emergencyStop = False  
				self.led.colorWipe(self.led.strip, Color(0,0,0),10)

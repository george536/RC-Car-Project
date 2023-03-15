from .UltrasonicObserver import *
from MQTT.CarInfo import CarInfo
from MQTT.topics import Topic
from LED.LED import Led


class CollisionDetection(UltrasonicObserver):
	def __init__(self,observerManager):
		super().__init__()
		self.observerManager = observerManager
		observerManager.attach(self)
		self.likelyhood = 0
		self.minimum = 15 # default minimum distance in cm
		led = Led()

	def update(self):
		if ultrasonic.get_distance() <=self.minimum:
		    self.likelyhood += 1
		    if self.likelyhood >=2:
			    self.likelyhood = 0
			    self.observerManager.emergencyStop = True
				led.colorWipe(led.strip, Color(255, 0, 0))
			    PWM.setMotorModel(0,0,0,0)
			    print("Emergency Stop")
		else:
			led.colorWipe(led.strip, Color(0, 0, 0), 10)
			if self.observerManager.emergencyStop == True:
				self.observerManager.emergencyStop = False

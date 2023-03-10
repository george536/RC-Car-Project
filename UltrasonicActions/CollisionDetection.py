from .UltrasonicObserver import *
from MQTT.CarInfo import CarInfo
from MQTT.topics import Topic

class CollisionDetection(UltrasonicObserver):
	
	def __init__(self,observerManager):
		super().__init__()
		self.observerManager = observerManager
		observerManager.attach(self)
		self.likelyhood = 0
		self.minimum = 15 # default minimum distance in cm
		
	def update(self):
		if ultrasonic.get_distance() <=self.minimum:
		    self.likelyhood += 1
		    if self.likelyhood >=5:
			    #self.observerManager.mqttClient.publish(f"{str(Topic.Main.value)}/{str(Topic.EMERGENCYSTOP.value)}/{str(CarInfo.carId)}", payload=str(1), qos=1)
			    self.likelyhood = 0
			    self.observerManager.emergencyStop = True
			    PWM.setMotorModel(0,0,0,0)
			    print("Emergency Stop")
		else:
			if self.observerManager.emergencyStop == True:
				#self.observerManager.mqttClient.publish(f"{str(Topic.Main.value)}/{str(Topic.EMERGENCYSTOP.value)}/{str(CarInfo.carId)}", payload=str(0), qos=1)
			    self.observerManager.emergencyStop = False 
			#self.observerManager.emergencyStop = False  

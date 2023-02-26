
class ObserverManager:
	
	def __init__(self):
		self.observers = []
		self.emergencyStop = False
		self.mqttClient = None
		
	def getEmergencyStopState(self):
		return self.emergencyStop
		
	def attach(self, observer):
		self.observers.append(observer)
		
	def notifyAllObservers(self):
		for observer in self.observers:
			observer.update()

	def setMqttClient(self,client):
		self.mqttClient = mqttClient
		

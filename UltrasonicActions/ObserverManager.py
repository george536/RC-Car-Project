
class ObserverManager:
	
	def __init__(self):
		self.observers = []
		self.emergencyStop = False
		
	def getEmergencyStopState(self):
		return self.emergencyStop
		
		
	def attach(self, observer):
		self.observers.append(observer)
		
	def notifyAllObservers(self):
		for observer in self.observers:
			observer.update()
		

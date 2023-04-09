from abc import ABC, abstractmethod
from RcCarModules.Line_Tracking import *

class PathObserver(ABC):
	
	def __init__(self,ultrasonicManager,egoCar):
		self.observerManager = None
		self.TrackingModule = Line_Tracking()
		self.ultrasonicManager = ultrasonicManager
		self.egoCar = egoCar
		
	@abstractmethod
	def update(self):
            pass

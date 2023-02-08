from abc import ABC, abstractmethod
from RcCarModules.Line_Tracking import *

class PathObserver(ABC):
	
	def __init__(self,ultrasonicManager):
		self.observerManager = None
		self.TrackingModule = Line_Tracking()
		self.ultrasonicManager = ultrasonicManager
		
	@abstractmethod
	def update(self):
            pass

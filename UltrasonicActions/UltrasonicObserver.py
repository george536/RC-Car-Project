from abc import ABC, abstractmethod
from RcCarModules.Ultrasonic import *
from RcCarModules.Motor import *

class UltrasonicObserver(ABC):
	
	def __init__(self):
		self.observerManager = None
		
	@abstractmethod
	def update(self):
            pass

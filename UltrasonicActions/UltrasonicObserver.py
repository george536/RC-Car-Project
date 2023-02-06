from abc import ABC, abstractmethod
import sys
sys.path.append("/home/pi/Documents/RcCode/RcCarModules")
from Ultrasonic import *
from Motor import *

class UltrasonicObserver(ABC):
	
	def __init__(self):
		self.observerManager = None
		
	@abstractmethod
	def update(self):
            pass

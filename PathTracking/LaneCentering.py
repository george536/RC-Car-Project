from .PathObserver import *
from .Positions import Position
from CarControls.CarCommands import *

class LaneCentering(PathObserver):
	
	def __init__(self,observerManager,ultrasonicManager):
		super().__init__(ultrasonicManager)
		self.observerManager = observerManager
		observerManager.attach(self)
		
	def update(self):
            while True:
                if self.ultrasonicManager.getEmergencyStopState()==False:
			
                    if self.TrackingModule.getPosition()==Position.Left:
                        CarCommands.turn(-5)
                    elif self.TrackingModule.getPosition()==Position.Right:
                        CarCommands.turn(5)

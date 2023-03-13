from .PathObserver import *
from .Positions import Position
from CarControls.CarCommands import *
from RcCarModules.Motor import *

class LaneCentering(PathObserver):
	
	def __init__(self,observerManager,ultrasonicManager,egoCar):
		super().__init__(ultrasonicManager,egoCar)
		self.observerManager = observerManager
		observerManager.attach(self)
		self.ctrl = CarCommands(ultrasonicManager)
		
	def update(self):

            if self.ultrasonicManager.getEmergencyStopState()==False:
                self.TrackingModule.run(self.egoCar.getScaledSpeed())
            else:
                self.egoCar.setSpeed(0)
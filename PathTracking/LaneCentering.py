from .PathObserver import *
from .Positions import Position
from CarControls.CarCommands import *
from RcCarModules.Motor import *

class LaneCentering(PathObserver):
	
	def __init__(self,observerManager,ultrasonicManager):
		super().__init__(ultrasonicManager)
		self.observerManager = observerManager
		observerManager.attach(self)
		self.ctrl = CarCommands(ultrasonicManager)
		
	def update(self):
            while True:
                if self.ultrasonicManager.getEmergencyStopState()==False:
                    self.TrackingModule.getPosition()
                    #if self.TrackingModule.getPosition()==Position.Left:
                        
                        #PWM.setMotorModel(1500,1500,-2500,-2500)
                        #pass
                        #self.ctrl.turn(-5)
                    #elif self.TrackingModule.getPosition()==Position.Right:
                        
                        #PWM.setMotorModel(-2500,-2500,1500,1500)
                        #pass
                        #self.ctrl.turn(5)

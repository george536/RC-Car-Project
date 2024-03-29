
from RcCarModules.Motor import *
# These functions were not used, only the stop function
# Please do not use this code as it has no usueful use, was initially used for testing
class CarCommands:
	
	def __init__(self, ultrasonicManager):
		self.ultrasonicManager = ultrasonicManager
	
	def turn(self,angle):
		if self.ultrasonicManager.getEmergencyStopState()==True:
					return
		if angle>0:
			PWM.setMotorModel(-2000,-2000,500,500)
			time.sleep(abs(angle)/90)
		else:
			PWM.setMotorModel(500,500,-2000,-2000)
			time.sleep(abs(angle)/90)
			
			
	def DriveForward(self,speed):
		if self.ultrasonicManager.getEmergencyStopState()==True:
					return
		speed=-1*speed
		PWM.setMotorModel(speed,speed,speed,speed)
		

	def DriveBackward(self,speed):
		if self.ultrasonicManager.getEmergencyStopState()==True:
					return
		PWM.setMotorModel(speed,speed,speed,speed)
		

	def stop(self):
		PWM.setMotorModel(0,0,0,0)
		

	def changeSpeed(self,initial_speed, final_speed, acceleration_rate, time):
		if initial_speed < final_speed:
			speed = initial_speed
			t = 0
			while speed < final_speed:
				
				if self.ultrasonicManager.getEmergencyStopState()==True:
					break
					
				t += time
				speed = initial_speed + int(acceleration_rate * t)
				self.DriveForward(speed)
		else:
			speed = initial_speed
			t = 0
			while speed > final_speed:
				
				if self.ultrasonicManager.getEmergencyStopState()==True:
					break
					
				t += time
				speed = initial_speed - int(acceleration_rate * t)
				self.DriveForward(speed)
			
		
			
	
	
	
	
		
		
		
		
		

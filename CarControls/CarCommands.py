import sys
sys.path.append("/home/pi/Documents/RcCode/RcCarModules")
from Motor import *

class CarCommands:
	
	def __init__(self, collisionObserver):
		self.collisionObserver = collisionObserver
	
	def turn(self,angle):
		if self.collisionObserver.getEmergencyStopState()==True:
					return
		if angle>0:
			PWM.setMotorModel(-2000,-2000,500,500)
			time.sleep(abs(angle)/90)
		else:
			PWM.setMotorModel(500,500,-2000,-2000)
			time.sleep(abs(angle)/90)
			
			
	def DriveForward(self,speed):
		if self.collisionObserver.getEmergencyStopState()==True:
					return
		speed=-1*speed
		PWM.setMotorModel(speed,speed,speed,speed)
		

	def DriveBackward(self,speed):
		if self.collisionObserver.getEmergencyStopState()==True:
					return
		PWM.setMotorModel(speed,speed,speed,speed)
		

	def stop(self):
		PWM.setMotorModel(0,0,0,0)
		

	def changeSpeed(self,initial_speed, final_speed, acceleration_rate, time):
		if initial_speed < final_speed:
			speed = initial_speed
			t = 0
			while speed < final_speed:
				
				if self.collisionObserver.getEmergencyStopState()==True:
					break
					
				t += time
				speed = initial_speed + int(acceleration_rate * t)
				self.DriveForward(speed)
		else:
			speed = initial_speed
			t = 0
			while speed > final_speed:
				
				if self.collisionObserver.getEmergencyStopState()==True:
					break
					
				t += time
				speed = initial_speed - int(acceleration_rate * t)
				self.DriveForward(speed)
			
		
			
	
	
	
	
		
		
		
		
		

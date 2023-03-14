from CarControls.CarCommands import CarCommands
from UltrasonicActions.CollisionDetection import CollisionDetection 
#from UltrasonicActions.LeadCarDetection import LeadCarDetection 
from UltrasonicActions.ObserverManager import ObserverManager as UltrasonicManager
from PathTracking.LaneCentering import LaneCentering
from PathTracking.ObserverManager import ObserverManager as PathManager
import HelperFunctions.SpeedScale as speedScale
from threading import Thread
import time
import sys
import os
from RcCarModules.Motor import *
from MQTT.mqtt import MQTTCommunication
from MQTT.topics import Topic
from MQTT.CarInfo import CarInfo
from CameraLaneDetection.CameraLaneDetection import CameraLaneDetection
from CameraLaneDetection.CamLaneTracking import CamLaneTracking

# driving scenario thread
class DrivingScenario(Thread):
	def __init__(self,ultrasonicManager,egoCar):
		super().__init__()
		# ultrasonicManager manager is the observer that checks for emergency stops
		self.ctrl = CarCommands(ultrasonicManager)
		self.egoCar = egoCar
		
	def run(self):
            while True:
            	self.ctrl.DriveForward(speedScale.scaleToRC(self.egoCar.getSpeed()))

# Collision detection thread
class detectCollision(Thread):
	def __init__(self,ultrasonicManager):
		super().__init__()
		
		self.observerManager = ultrasonicManager
		CollisionDetection(self.observerManager)
		#LeadCarDetection(self.observerManager)
		
	def run(self):
	
		while True:
			self.observerManager.notifyAllObservers()

# Tracking path thread
class TrackingPath(Thread):
	def __init__(self,observerManager,ultrasonicManager,egoCar):
		super().__init__()

		self.observerManager = observerManager
		LaneCentering(self.observerManager,ultrasonicManager,egoCar)

	def run(self):
		while True:
			self.observerManager.notifyAllObservers()

# thread to listen for mqtt messages
class MQTTRunner(Thread):
	def __init__(self,mqttClient):
		super().__init__()
		self.mqttClient=mqttClient

	def run(self):
		self.mqttClient.subscribe(f"{str(Topic.Main.value)}/{str(Topic.SPEED.value)}/{str(CarInfo.carId)}", qos=1)
		self.mqttClient.loop_forever()

class CameraDetection(Thread):
	def __init__(self,ultrasonicManager,egoCar):
		super().__init__()
		self.CamLaneTracking = CamLaneTracking(ultrasonicManager,egoCar)

	def run(self):
		while True:
			self.CamLaneTracking.update()


# this class represents the car running this code
class Egocar:
	def __init__(self):
		# speed in Km/h
		self.speed = 20

	def getSpeed(self):
		return self.speed

	def setSpeed(self,newSpeed):
		#print(f"changing speed to {newSpeed}")
		self.speed = newSpeed

	def getScaledSpeed(self):
		return speedScale.scaleToRC(self.speed)
		
def main():
	
    threads = []
	# MQTT passed in to send data back to server
    ultrasonicManager = UltrasonicManager()
    pathManager = PathManager()
    egoCar = Egocar()

    mqtt = MQTTCommunication(egoCar,ultrasonicManager)
    global mqttClient
    mqttClient = mqtt.getClient()

    #threads.append(DrivingScenario(ultrasonicManager,egoCar))
    threads.append(detectCollision(ultrasonicManager))
    #threads.append(TrackingPath(pathManager,ultrasonicManager,egoCar))
    #threads.append(MQTTRunner(mqttClient))
    threads.append(CameraLaneDetection())
    threads.append(CameraDetection(ultrasonicManager,egoCar))


    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


try: 
    main()
except Exception as e:
    print(e)
    PWM.setMotorModel(0,0,0,0)
    PWM.setMotorModel(0,0,0,0)
    PWM.setMotorModel(0,0,0,0)
    PWM.setMotorModel(0,0,0,0)

    try:
        sys.exit(130)
    except SystemExit:
        os._exit(130)













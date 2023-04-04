from CarControls.CarCommands import CarCommands
from UltrasonicActions.CollisionDetection import CollisionDetection 
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
from CameraLaneDetection.PIDTuning import SliderInterface
import signal

# Collision detection thread
class detectCollision(Thread):
	def __init__(self,ultrasonicManager):
		super().__init__()
		
		self.observerManager = ultrasonicManager

		# modify these values to change settings of emergency stopping
		stoppingDistance = 5
		likelihoodBound=7

		CollisionDetection(self.observerManager,stoppingDistance,likelihoodBound)
		
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


class Slider(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        slider_interface = SliderInterface()


# this class represents the car running this code
class Egocar:
	def __init__(self):
		# speed in Km/h
		self.speed =0

	def getSpeed(self):
		return self.speed

	def setSpeed(self,newSpeed):
		self.speed = newSpeed

	def getScaledSpeed(self):
		return speedScale.scaleToRC(self.speed)
		
def main():
	
    threads = []

    ultrasonicManager = UltrasonicManager()
    pathManager = PathManager()
    egoCar = Egocar()

    mqtt = MQTTCommunication(egoCar,ultrasonicManager)
    global mqttClient
    mqttClient = mqtt.getClient()

    threads.append(detectCollision(ultrasonicManager))
    threads.append(MQTTRunner(mqttClient))
    threads.append(CameraLaneDetection())
    threads.append(CameraDetection(ultrasonicManager,egoCar))

    if "-testPID" in sys.argv:
        threads.append(Slider())


    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


def signal_handler(sig, frame):
    carCommands = CarCommands(UltrasonicManager())
    # Exit all threads
    for _ in range(4):
    	carCommands.stop()
    # Exit the main thread
    sys.exit()
    raise SystemExit


signal.signal(signal.SIGINT, signal_handler)

main()















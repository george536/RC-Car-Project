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
from MQTT.mqtt import MQTTCommunication
from MQTT.topics import Topic
from MQTT.CarInfo import CarInfo
from CameraLaneDetection.CameraLaneDetection import CameraLaneDetection
from CameraLaneDetection.CamLaneTracking import CamLaneTracking
from CameraLaneDetection.PIDTuning import SliderInterface
from CameraLaneDetection.TrafficLightDetector import TrafficLightDetector
import signal

# Collision detection thread
class detectCollision(Thread):
	def __init__(self,ultrasonicManager):
		super().__init__()
		
		self.observerManager = ultrasonicManager

		# modify these values to change settings of emergency stopping
		stoppingDistance = 4
		likelihoodBound=3

		CollisionDetection(self.observerManager,stoppingDistance,likelihoodBound)
		
	def run(self):
		while True:
			self.observerManager.notifyAllObservers()

# Tracking path thread, currently not used
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
		self.mqttClient.subscribe(f"{str(Topic.Main.value)}/{str(Topic.TRAFFICLIGHT.value)}/{str(Topic.RED.value)}", qos=1)
		self.mqttClient.subscribe(f"{str(Topic.Main.value)}/{str(Topic.TRAFFICLIGHT.value)}/{str(Topic.YELLOW.value)}", qos=2)
		self.mqttClient.loop_forever()

# path tracking thread throgh the camera
class CameraDetection(Thread):
	def __init__(self,ultrasonicManager,egoCar):
		super().__init__()
		self.CamLaneTracking = CamLaneTracking(ultrasonicManager,egoCar)

	def run(self):
		while True:
			self.CamLaneTracking.update()


# PID tuning slider with speed controller
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

	# this return speed equivalence in PWM 
	def getScaledSpeed(self):
		return speedScale.scaleToRC(self.speed)
		
def main():
	
    threads = []

    ultrasonicManager = UltrasonicManager()
	# not used (relates to car stock tracking module)
    # pathManager = PathManager()
    egoCar = Egocar()

	# mqtt communication client
    mqtt = MQTTCommunication(egoCar,ultrasonicManager)
    global mqttClient
    mqttClient = mqtt.getClient()

    threads.append(detectCollision(ultrasonicManager))
    threads.append(MQTTRunner(mqttClient))
    threads.append(CameraLaneDetection())
    threads.append(CameraDetection(ultrasonicManager,egoCar))
    threads.append(TrafficLightDetector())
	
	# calling option -testPID will show the slider
    if "-testPID" in sys.argv:
        threads.append(Slider())


    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

# used to handle closing signals, and then to stop the car
def signal_handler(sig, frame):
	# this ultasonic manager is not attached to any observers, we only need this to use the stop function
    carCommands = CarCommands(UltrasonicManager())
    # 4 was random, use as many as needed so it stops, there seems to be a delay from the PI
	# and doesn't stop sometimes
    for _ in range(4):
        carCommands.stop()
    # Exit the main thread
    sys.exit()
    raise SystemExit


signal.signal(signal.SIGINT, signal_handler)

main()



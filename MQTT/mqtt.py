
import time
import paho.mqtt.client as paho
from paho import mqtt
from .CarInfo import CarInfo 
from .topics import Topic
from HelperFunctions.CalculateDistance import *
from CameraLaneDetection.DetectionData import DetectionData

class MQTTCommunication:

    def __init__(self,car,ultrasonicManager):
        self.client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
        self.client.on_connect = self.on_connect

        # enable TLS for secure connection
        self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        # set username and password
        self.client.username_pw_set("mcmaster", "McMaster123")
        # connect to HiveMQ Cloud on port 8883 (default for MQTT)
        self.client.connect("5a3cea1ebc484e859be394be5b862daf.s2.eu.hivemq.cloud", 8883)

        # setting callbacks, use separate functions like above for better visibility
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish

        self.car = car
        self.ultrasonicManager = ultrasonicManager

    def getClient(self):
        return self.client

    # setting callbacks for different events to see if it works, print the message etc.
    def on_connect(self,client, userdata, flags, rc, properties=None):
        print("CONNACK received with code %s." % rc)

    # with this callback you can see if your publish was successful
    def on_publish(self,client, userdata, mid, properties=None):
        return
        print("mid: " + str(mid))

    # print which topic was subscribed to
    def on_subscribe(self,client, userdata, mid, granted_qos, properties=None):
        return 
        print("Subscribed: " + str(mid) + " " + str(granted_qos))

    # print message, useful for checking if it was successful
    def on_message(self,client, userdata, msg):
        # Speed messages
        speed_pattern = f"{str(Topic.Main.value)}/{str(Topic.SPEED.value)}/{str(CarInfo.carId)}"

        if speed_pattern==msg.topic:
            if self.ultrasonicManager.getEmergencyStopState()==False:
                self.car.setSpeed(float(msg.payload.decode()))
                client.publish(f"{str(Topic.Main.value)}/{str(Topic.DISTANCE.value)}/{str(CarInfo.carId)}", payload=str(calcDistance(self.car.getScaledSpeed(),0.3)), qos=1)
                client.publish(f"{str(Topic.Main.value)}/{str(Topic.EMERGENCYSTOP.value)}/{str(CarInfo.carId)}", payload=str(0), qos=1)
            else:
                self.car.setSpeed(0)
                client.publish(f"{str(Topic.Main.value)}/{str(Topic.DISTANCE.value)}/{str(CarInfo.carId)}", payload=str(0), qos=1)
                client.publish(f"{str(Topic.Main.value)}/{str(Topic.EMERGENCYSTOP.value)}/{str(CarInfo.carId)}", payload=str(1), qos=1)


        # Traffic Light messages
        red_pattern = f"{str(Topic.Main.value)}/{str(Topic.TRAFFICLIGHT.value)}/{str(Topic.RED.value)}"
        yellow_pattern = f"{str(Topic.Main.value)}/{str(Topic.TRAFFICLIGHT.value)}/{str(Topic.YELLOW.value)}"
        if red_pattern==msg.topic:
            DetectionData.CurrentTraffic['red'] = bool(msg.payload.decode())
            DetectionData.CurrentTraffic['yellow'] = not bool(msg.payload.decode())
        if yellow_pattern==msg.topic:
            DetectionData.CurrentTraffic['red'] = not bool(msg.payload.decode())
            DetectionData.CurrentTraffic['yellow'] = bool(msg.payload.decode())




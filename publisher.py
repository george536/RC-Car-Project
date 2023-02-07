import paho.mqtt.client as mqtt
from random import randrange, uniform
import time

mqttBroker ="mqtt.eclipseprojects.io"

client = mqtt.Client("Car-1")
client.connect(mqttBroker)

while True:
    randNumber = uniform(20.0, 50.0)
    client.publish("SPEED", randNumber)
    print("Just published " + str(randNumber) + " to topic SPEED")
    # time.sleep(1)
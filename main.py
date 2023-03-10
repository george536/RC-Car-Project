from Gipps_Vehicle import Gipps_Vehicle
from GippsModel import GippsModel
from guiControls import App
from tkinter import *
from threading import Thread
from vars import Vars
import csv
import os
from datetime import datetime
import time
from mqtt import MQTTCommunication
from topics import Topic

MqttPeriod = 0.3

def insert_into_csv(data):
    if not os.path.exists("plot.csv"):
        with open("plot.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)
        return

    with open('plot.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)  

# Multithreaded call for app GUI
class AppRunner(Thread):
    def __init__(self, cars, model):
        super().__init__()
        self.app = None
        self.cars = cars
        self.model = model

    def run(self):
        # GUI init
        self.app = App(Tk(), self.cars, self.model)

# Multithreaded call for updating the cars
class ModelRunner(Thread):
    def __init__(self, model, cars):
        super().__init__()

        self.model = model
        self.cars = cars
        self.log = "log.txt"

        # csv header
        header = ["Steps"]

        # assigning car followers
        for i in range(len(cars)-1):
            cars[i].follower = cars[i+1]
            # creating csv file header
            header.append(f"Car {i+1}")

        header.append(f"Car {i+2}")

        insert_into_csv(header)

        # craeting time steps for plot creation
        self.lastCheckPoint = datetime.now()
        self.initialCheckPoint = datetime.now()

    def run(self):

        while True:
            # to be deleted
            time.sleep(MqttPeriod)
            # car id
            for car in self.cars:

                # TO BE ADDED AFTER CAR CODE SENDS IT
                car.loc += Vars.over_mqtt_distances[car.idx-1]
                # reset
                Vars.over_mqtt_distances[car.idx-1] = 0

                # updating car info and counter id
                car.update()

                # emergency stop
                if Vars.over_mqtt_emergency_stops[car.idx-1] == 1:
                    car.v = 0
                    car.loc=0
                    car.loc = car.calc_loc()

                global mqttClient
                # send speed commands
                mqttClient.publish(f"{str(Topic.Main.value)}/{str(Topic.SPEED.value)}/{str(car.idx)}", payload=str(self.model.get_speed(car)), qos=1)
                # store speeds to be graphed
                Vars.speeds[car.idx-1] = self.model.get_speed(car)
                
                # update distance recieved
                # TO BE ADDED AFTER CAR CODE SENDS IT
                #car.loc += Vars.over_mqtt_distances[car.idx-1]
                #Vars.over_mqtt_distances[car.idx-1] = 0

            current = datetime.now()
            if (current - self.lastCheckPoint).total_seconds() >= 0.5:
                data = [(current - self.initialCheckPoint).total_seconds()]
                for i in range(len(Vars.speeds)):
                    print(f"car {i+1} speed "+str(Vars.speeds[i])+"\n")
                    #print(f"car {i+1} location "+str(self.cars[i].loc)+"\n")
                    data.append(Vars.speeds[i])
                insert_into_csv(data)
                self.lastCheckPoint = datetime.now()

class MQTTRunner(Thread):
    def __init__(self,mqttClient,cars):
        super().__init__()
        self.mqttClient=mqttClient
        self.cars=cars

    def run(self):
        for car in self.cars:
            # listen for distances
            self.mqttClient.subscribe(f"{str(Topic.Main.value)}/{str(Topic.DISTANCE.value)}/{str(car.idx)}", qos=1)
            self.mqttClient.subscribe(f"{str(Topic.Main.value)}/{str(Topic.EMERGENCYSTOP.value)}/{str(car.idx)}", qos=1)
                                      
        self.mqttClient.loop_forever()

def main():

    model = GippsModel()
    car1 = Gipps_Vehicle(1, 50, model, None)
    car2 = Gipps_Vehicle(2, 50, model, car1)

    cars = [car1,car2]

    Vars.speeds = [0,0]

    Vars.over_mqtt_distances = [0,0]

    Vars.over_mqtt_emergency_stops = [0,0]

    threads = []

    appRunner = AppRunner(cars,model)
    threads.append(appRunner)

    modelRunner = ModelRunner(model,cars)
    threads.append(modelRunner)

    mqtt = MQTTCommunication()
    global mqttClient
    mqttClient = mqtt.getClient()

    mqttRunner = MQTTRunner(mqttClient,cars)
    threads.append(mqttRunner)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


main()


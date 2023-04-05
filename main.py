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
import sys

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

        global save_to_csv
        if save_to_csv:
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
                

            current = datetime.now()
            if (current - self.lastCheckPoint).total_seconds() >= 0.5:
                data = [(current - self.initialCheckPoint).total_seconds()]

                for i in range(len(Vars.speeds)):
                    print(f"car {i+1} speed "+str(Vars.speeds[i])+"\n")

                    data.append(Vars.speeds[i])
                    
                global save_to_csv
                if save_to_csv:
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
        

class TrafficSignal(Thread):
    def __init__(self,mqttClient):
        super().__init__()
        self.mqttClient=mqttClient
        # Traffic light timer
        self.traffic_light_last_time = time.time()
        self.traffic_light_period = 3
        self.trafficFlow = {
            'yellow': False,
            'red':True
        }

    def run(self):
        while True:
            if (time.time() - self.traffic_light_last_time) >= self.traffic_light_period:
                self.traffic_light_last_time = time.time()
                self.trafficFlow['yellow'] = not self.trafficFlow['yellow']
                self.trafficFlow['red'] = not self.trafficFlow['red']
                self.mqttClient.publish(f"{str(Topic.Main.value)}/{str(Topic.TRAFFICLIGHT.value)}/{str(Topic.YELLOW.value)}", payload=str(self.trafficFlow['yellow']), qos=1)
                self.mqttClient.publish(f"{str(Topic.Main.value)}/{str(Topic.TRAFFICLIGHT.value)}/{str(Topic.RED.value)}", payload=str(self.trafficFlow['red']), qos=2)


def main():

    model = GippsModel()

    initial_speed = 0
    num_of_cars = 0

    if "-#" in sys.argv:
        try:
            num_of_cars = int(sys.argv[sys.argv.index("-#") + 1])
        except:
            print("Invalid number of cars")
            return
    else:
        print("you must enter the number of cars")

    
    if "-v" in sys.argv:
        try:
            initial_speed = int(sys.argv[sys.argv.index("-v") + 1])
        except:
            print("Invalid speed")
            return

    global save_to_csv
    save_to_csv = False

    if "-csv" in sys.argv:
        save_to_csv = True

    cars = []
    for i in range(num_of_cars):

        lead = None
        if i > 0:
            lead = cars[i-1]

        cars.append(Gipps_Vehicle(i+1, initial_speed, model, lead))

        Vars.speeds.append(0)

        Vars.over_mqtt_distances.append(0)

        Vars.over_mqtt_emergency_stops.append(0)

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

    threads.append(TrafficSignal(mqttClient))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


main()


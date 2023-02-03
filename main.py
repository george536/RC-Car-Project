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
            time.sleep(0.3)
            # car id
            id = 1
            for car in self.cars:

                # saving to log
                #f = open(self.log, "a")
                #f.write(f"car {id} speed "+str(self.model.get_speed(car))+"\n")
                #f.close()

                # updating car info and counter id
                car.update()
                Vars.speeds[id-1] = self.model.get_speed(car)

                id+=1

            current = datetime.now()
            if (current - self.lastCheckPoint).total_seconds() >= 0.5:
                data = [(current - self.initialCheckPoint).total_seconds()]
                for i in range(len(Vars.speeds)):
                    print(f"car {i+1} speed "+str(Vars.speeds[i])+"\n")
                    data.append(Vars.speeds[i])
                insert_into_csv(data)
                self.lastCheckPoint = datetime.now()



def main():

    model = GippsModel()
    car1 = Gipps_Vehicle(1, 50, model, None)
    car2 = Gipps_Vehicle(2, 50, model, car1)
    car3 = Gipps_Vehicle(3, 50, model, car2)

    cars = [car1,car2,car3]

    Vars.speeds = [0,0,0]

    threads = []

    appRunner = AppRunner(cars,model)
    threads.append(appRunner)

    modelRunner = ModelRunner(model,cars)
    threads.append(modelRunner)


    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


main()


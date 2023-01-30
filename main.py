from Gipps_Vehicle import Gipps_Vehicle
from GippsModel import GippsModel
from guiControls import App
from tkinter import *
from threading import Thread
import time
from vars import Vars
import csv
import os

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
    def __init__(self):
        super().__init__()
        self.app = None

    def run(self):
        # GUI init
        self.app = App(Tk())

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
            header.append(f"Car {i+1}")

        header.append(f"Car {i+2}")

        insert_into_csv(header)

    def run(self):
        # num of updates since beginning
        num_updates = 0
        steps = 0
        c = 0
        # previous value to print every 10 units of speed 
        prev = 0
        while True:

            num_updates+=1

            # car id
            counter = 1
            for car in self.cars:
                if(abs(self.model.get_speed(car)-prev)>10) and counter==1:
                    prev = self.model.get_speed(car)
                    print(f"car {counter} speed is: "+str(self.model.get_speed(car))+"\n")

                # saving to log
                f = open(self.log, "a")
                f.write(f"car {counter} speed "+str(self.model.get_speed(car))+"\n")
                f.close()

                # updating car info and counter id
                car.update()
                Vars.speeds[counter-1] = self.model.get_speed(car)

                counter+=1

                # change cars speed
                if counter==2 and num_updates>10000 and self.model.get_speed(car)>48:
                    print("############# changing speed ############")
                    num_updates = 0
                    car.max_v = 30

            c+=1

            if c>100:
                data = [steps]
                for speed in Vars.speeds:
                    data.append(speed)
                insert_into_csv(data)
                steps+=1
                c=0



def main():
    model = GippsModel()
    car1 = Gipps_Vehicle(0, 50, model, None)
    car2 = Gipps_Vehicle(1, 50, model, car1)
    car3 = Gipps_Vehicle(2, 50, model, car2)

    cars = [car1,car2,car3]

    Vars.speeds = [0,0,0]

    threads = []

    appRunner = AppRunner()
    threads.append(appRunner)

    modelRunner = ModelRunner(model,cars)
    threads.append(modelRunner)


    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


main()


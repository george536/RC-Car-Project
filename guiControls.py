import tkinter as tk
from vars import Vars as v

# this will be used by GUI for controlling cars
class CarControl:
    def __init__(self,car, model):
        self.car = car
        self.model = model
        self.intended_speed = self.car.max_v
        self.breaking = False

    def get_speed(self):
        self.intended_speed = self.car.max_v
        return self.intended_speed

    def update_intended_speed(self,new_speed):
        self.car.max_v = int(new_speed)
        self.intended_speed = new_speed

    def start_sudden_breaking(self,id,elemid):

        if self.breaking:
            self.car.stop_sundden_braking()
            self.breaking = False
            carUIElements[id][elemid].config(text="Start Breaking")
        else:
            self.breaking = True
            self.car.start_sundden_braking()
            carUIElements[id][elemid].config(text="Stop Breaking")
            


def update_greatest_speed_reduction(value):
    v.Greatest_speed_reduction = float(value)

def update_Zone_of_influence_upstream(value):
    v.Zone_of_influence_upstream = float(value)

def update_Zone_of_influence_downstream(value):
    v.Zone_of_influence_downstream = float(value)

def update_length(value):
    v.length = float(value)

def update_miniGap(value):
    v.miniGap = float(value)

def update_initialMaxBraking():
    if(initialMaxBraking.get()==0):
        v.initialMaxBraking = False
        return
    v.initialMaxBraking = True

def update_driver_reaction_time(value):
    v.driver_reaction_time = float(value)

def update_randomness():
    if(randomness.get()==0):
        v.randomness = False
        return
    v.randomness = True

def update_max_acceleration(value):
    v.max_acceleration = float(value)

def update_efffective_size(value):
    v.efffective_size = float(value)

class App:
    def __init__(self, master, cars, model):
        self.master = master
        self.cars = cars
        self.model = model

        master.title("Variables Controls")

        self.label1 = tk.Label(master, text="Greatest Speed Reduction")
        self.label1.grid(row=0, column=0)

        self.scale1 = tk.Scale(master, from_=0, to=5, resolution=0.01, orient='horizontal', variable=v.Greatest_speed_reduction, command = update_greatest_speed_reduction)
        self.scale1.grid(row=1, column=0)
        self.scale1.set(v.Greatest_speed_reduction)

        self.label2 = tk.Label(master, text="Zone of Influence Upstream")
        self.label2.grid(row=2, column=0)

        self.scale2 = tk.Scale(master, from_=0, to=30, resolution=0.01, orient='horizontal', variable=v.Zone_of_influence_upstream, command = update_Zone_of_influence_upstream)
        self.scale2.grid(row=3, column=0)
        self.scale2.set(v.Zone_of_influence_upstream)

        self.label3 = tk.Label(master, text="Zone of Influence Downstream")
        self.label3.grid(row=4, column=0)

        self.scale3 = tk.Scale(master, from_=0, to=30, resolution=0.01, orient='horizontal', variable=v.Zone_of_influence_downstream, command = update_Zone_of_influence_downstream)
        self.scale3.grid(row=5, column=0)
        self.scale3.set(v.Zone_of_influence_downstream)

        self.label4 = tk.Label(master, text="Vehicle Length")
        self.label4.grid(row=6, column=0)

        self.scale4 = tk.Scale(master, from_=0, to=50, resolution=0.01, orient='horizontal', variable=v.length, command = update_length)
        self.scale4.grid(row=7, column=0)
        self.scale4.set(v.length)

        self.label5 = tk.Label(master, text="Mini Gap")
        self.label5.grid(row=8, column=0)

        self.scale5 = tk.Scale(master, from_=0, to=20, resolution=0.01, orient='horizontal', variable=v.miniGap, command = update_miniGap)
        self.scale5.grid(row=9, column=0)
        self.scale5.set(v.miniGap)

        self.label6 = tk.Label(master, text="Initial Max Braking")
        self.label6.grid(row=10, column=0)

        global initialMaxBraking
        initialMaxBraking = tk.IntVar()
        if v.initialMaxBraking:
            initialMaxBraking.set(1)  
        else:
            initialMaxBraking.set(0)  

        self.scale6 = tk.Checkbutton(master, text="On/Off", variable=initialMaxBraking, command=update_initialMaxBraking)
        self.scale6.grid(row=11, column=0)

        self.label7 = tk.Label(master, text="Driver Reaction Time")
        self.label7.grid(row=12, column=0)

        self.scale7 = tk.Scale(master, from_=0, to=2, resolution=0.01, orient='horizontal', variable=v.driver_reaction_time, command = update_driver_reaction_time)
        self.scale7.grid(row=13, column=0)
        self.scale7.set(v.driver_reaction_time)

        self.label8 = tk.Label(master, text="Randomness")
        self.label8.grid(row=0, column=1)

        global randomness
        randomness = tk.IntVar()
        randomness.set(0)  

        self.scale8 = tk.Checkbutton(master, text="On/Off", variable=randomness, command=update_randomness)
        self.scale8.grid(row=1, column=1)

        self.label9 = tk.Label(master, text="Max Acceleration")
        self.label9.grid(row=2, column=1)

        self.scale9 = tk.Scale(master, from_=0, to=10, resolution=0.01, orient='horizontal', variable=v.max_acceleration, command = update_max_acceleration)
        self.scale9.grid(row=3, column=1)
        self.scale9.set(v.max_acceleration)

        self.label10 = tk.Label(master, text="Effective Size")
        self.label10.grid(row=4, column=1)

        self.scale10 = tk.Scale(master, from_=0, to=30, resolution=0.01, orient='horizontal', variable=v.efffective_size, command = update_efffective_size)
        self.scale10.grid(row=5, column=1)
        self.scale10.set(v.efffective_size)


        # cars controls

        last = 0
        global carUIElements
        carUIElements = []
        for i in range(len(self.cars)):

            car_control = CarControl(self.cars[i], self.model)

            carUIElements.append([tk.Label(master, text=f"Car {i+1} Intended Speed")])
            carUIElements[i][0].grid(row=last+i, column=2)

            speed = tk.IntVar()
            carUIElements[i].append(tk.Scale(master, from_=0.1, to=260, resolution=1, orient='horizontal', variable=speed, command = car_control.update_intended_speed))
            carUIElements[i][1].grid(row=last+1+i, column=2)
            carUIElements[i][1].set(car_control.intended_speed)

            carUIElements[i].append(tk.Button(master, text="Sudden Break", command=lambda c=i:car_control.start_sudden_breaking(c,2)))
            carUIElements[i][2].grid(row=last+2+i, column=2)

            last = last+2+i


        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)
        self.master.columnconfigure(2, weight=1)

        self.master.mainloop()


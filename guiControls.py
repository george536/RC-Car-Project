import tkinter as tk
from vars import Vars as v

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
    def __init__(self, master):
        self.master = master
        master.title("Variables Controls")

        self.label1 = tk.Label(master, text="Greatest Speed Reduction")
        self.label1.pack()

        self.scale1 = tk.Scale(master, from_=0, to=5, resolution=0.01, orient='horizontal', variable=v.Greatest_speed_reduction, command = update_greatest_speed_reduction)
        self.scale1.pack()
        self.scale1.set(v.Greatest_speed_reduction)

        self.label2 = tk.Label(master, text="Zone of Influence Upstream")
        self.label2.pack()

        self.scale2 = tk.Scale(master, from_=0, to=30, resolution=0.01, orient='horizontal', variable=v.Zone_of_influence_upstream, command = update_Zone_of_influence_upstream)
        self.scale2.pack()
        self.scale2.set(v.Zone_of_influence_upstream)

        self.label3 = tk.Label(master, text="Zone of Influence Downstream")
        self.label3.pack()

        self.scale3 = tk.Scale(master, from_=0, to=30, resolution=0.01, orient='horizontal', variable=v.Zone_of_influence_downstream, command = update_Zone_of_influence_downstream)
        self.scale3.pack()
        self.scale3.set(v.Zone_of_influence_downstream)

        self.label4 = tk.Label(master, text="Vehicle Length")
        self.label4.pack()

        self.scale4 = tk.Scale(master, from_=0, to=50, resolution=0.01, orient='horizontal', variable=v.length, command = update_length)
        self.scale4.pack()
        self.scale4.set(v.length)

        self.label5 = tk.Label(master, text="Mini Gap")
        self.label5.pack()

        self.scale5 = tk.Scale(master, from_=0, to=20, resolution=0.01, orient='horizontal', variable=v.miniGap, command = update_miniGap)
        self.scale5.pack()
        self.scale5.set(v.miniGap)

        self.label6 = tk.Label(master, text="Initial Max Braking")
        self.label6.pack()

        global initialMaxBraking
        initialMaxBraking = tk.IntVar()
        initialMaxBraking.set(0)  

        self.scale6 = tk.Checkbutton(master, text="On/Off", variable=initialMaxBraking, command=update_initialMaxBraking)
        self.scale6.pack()

        self.label7 = tk.Label(master, text="Driver Reaction Time")
        self.label7.pack()

        self.scale7 = tk.Scale(master, from_=0, to=2, resolution=0.01, orient='horizontal', variable=v.driver_reaction_time, command = update_driver_reaction_time)
        self.scale7.pack()
        self.scale7.set(v.driver_reaction_time)

        self.label8 = tk.Label(master, text="Randomness")
        self.label8.pack()

        global randomness
        randomness = tk.IntVar()
        randomness.set(0)  

        self.scale8 = tk.Checkbutton(master, text="On/Off", variable=randomness, command=update_randomness)
        self.scale8.pack()

        self.label9 = tk.Label(master, text="Max Acceleration")
        self.label9.pack()

        self.scale9 = tk.Scale(master, from_=0, to=10, resolution=0.01, orient='horizontal', variable=v.max_acceleration, command = update_max_acceleration)
        self.scale9.pack()
        self.scale9.set(v.max_acceleration)

        self.label10 = tk.Label(master, text="Effective Size")
        self.label10.pack()

        self.scale10 = tk.Scale(master, from_=0, to=30, resolution=0.01, orient='horizontal', variable=v.efffective_size, command = update_efffective_size)
        self.scale10.pack()
        self.scale10.set(v.efffective_size)

        self.master.mainloop()


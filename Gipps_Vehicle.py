from Vehicle import Vehicle
from numpy import random as random
from vars import Vars as v

class Gipps_Vehicle(Vehicle):
    def __init__(self,
                 idx, # Vehicle ID
                 v_intend, # Vehicle desired speed
                 gipps,
                 leader=None,
                 driver_reaction_time=v.driver_reaction_time,
                 randomness=v.randomness,
                 length = v.length):
        an = v.max_acceleration # max acceleartion
        sn = v.efffective_size # effective size of the vehicle: 5(length) + 2(mini inter-vechile distance)
        miniGap = v.miniGap

        if randomness:
            an = self.pick_normal(an, 0.3) # max acceleration
            sn = self.pick_normal(sn, 0.3) # effective size
            miniGap = sn - length
            v_intend = self.pick_normal(v_intend, 3.2)  # indended speed, in m/s
        super().__init__(
            idx,
            leader,
            simulationStep=driver_reaction_time * 1000,
            max_v=v_intend,
            miniGap=miniGap,
            length=length)
        self.an = an
        self.connected = False
        self.sn = sn
        self.vi = self.max_v  # indended speed, in m/s
        self.bn = -2 * self.an  # max deceleration bn
        self.tn = driver_reaction_time  # the reaction time of driver, default is 2/3
        self.b_hat = min(-3.0, (self.bn - 3) / 2)
        self.model = gipps

    # Check for influence
    def pick_normal(self, mean, std):
        pickup = random.normal(mean, std)
        while pickup > mean + std or pickup < mean - std:
            pickup = random.normal(mean, std)
        return pickup

    def update(self):
        self.base_update()
        if self.maxBraking:
            new_a = self.bn # new_acceleration = self.desired_braking
            new_v = self.v + self.tn/2 * (self.a + new_a)
        else:
            new_v = self.model.get_speed(self)
        # new_a = 2 * (new_v - self.v) / self.tn - self.a
        new_a = (new_v - self.v) / self.tn # new acceleration
        # compute new location
        new_loc = self.loc + self.tn/2 * (self.v + new_v)
        self.a = new_a
        self.v = new_v
        self.loc = new_loc
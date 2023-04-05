import time

class DetectionData:

    location = 0

    first_time_loading = False

    kp = 0
    ki = 0
    kd = 0

    testSpeed = None

    img = None

    currentlyAt = {
        'yellow':False,
        'red':False
    }

    CurrentTraffic = {
        'yellow':False,
        'red':False,
    }
    

    def isStoppedAtTraffic():
        currentlyAt = DetectionData.currentlyAt
        CurrentTraffic = DetectionData.CurrentTraffic

        print("currently at" + str(currentlyAt))
        print("current mqtt traffic"+str(CurrentTraffic))

        if currentlyAt['yellow'] and not CurrentTraffic['yellow']:
            #print(f"stopped at yellow {time.time()}")
            return True
        elif currentlyAt['red'] and not CurrentTraffic['red']:
            #print(f"stopped at red {time.time()}")
            return True
        else:
            return False
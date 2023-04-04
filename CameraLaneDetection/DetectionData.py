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
        'yellow':None,
        'red':None,
    }

    def isStoppedAtTraffic():
        if currentlyAt['yellow'] == None or currentlyAt['red'] == None:
            return False
        if currentlyAt['yellow'] and CurrentTraffic['yellow']:
            print("stopped at yellow")
            return True
        elif currentlyAt['red'] and CurrentTraffic['red']:
            print("stopped at red")
            return True
        else:
            return False
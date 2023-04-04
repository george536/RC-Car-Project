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
        currentlyAt = DetectionData.currentlyAt
        CurrentTraffic = DetectionData.CurrentTraffic
        print(currentlyAt)
        print(CurrentTraffic)
        if CurrentTraffic['yellow'] == None or CurrentTraffic['red'] == None:
            return False
        if currentlyAt['yellow'] and CurrentTraffic['yellow']:
            print("stopped at yellow")
            return True
        elif currentlyAt['red'] and CurrentTraffic['red']:
            print("stopped at red")
            return True
        else:
            return False
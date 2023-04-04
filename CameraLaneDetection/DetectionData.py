import json

class DetectionData:
    with open('CameraLaneDetection/PIDparameters.json', 'r') as file:
        data = json.load(file)


    location = 0

    first_time_loading = False

    kp = 0
    ki = 0
    kd = 0

    if not first_time_loading:

        first_time_loading=True

        kp = data['kp']
        ki = data['ki']
        kd = data['kd']


    testSpeed = None
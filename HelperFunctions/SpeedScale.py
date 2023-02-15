def scaleToRC(speed):
    # 4096 is max
    # 120 km/hr is max
    max_car_speed = 120
    factor = (4096-400)/max_car_speed

    if speed >max_car_speed:
        return 4096

    scaledSpeed = speed*factor + 400

    return scaledSpeed

    


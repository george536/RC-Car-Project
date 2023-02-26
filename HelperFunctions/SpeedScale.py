from ScalingParameters import ScalingParameters

def scaleToRC(speed):

    if speed >ScalingParameters.max_car_speed:
        return ScalingParameters.max_RC_PWM

    factor = (ScalingParameters.max_RC_PWM-ScalingParameters.min_RC_PWM)/ScalingParameters.max_car_speed

    scaledSpeed = speed*factor + ScalingParameters.min_RC_PWM
    
    if scaledSpeed==ScalingParameters.min_RC_PWM:
        return 0

    return int(scaledSpeed)

    


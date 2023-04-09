from .ScalingParameters import ScalingParameters

# this is simply like a liear fucntion that scales the speed from km/h to PWM
# To ensure all RC cars have the same real speed, ensure the batteries are fully
# charged before running the mode :(
def scaleToRC(speed):

    if speed <1:
        return 0

    if speed >ScalingParameters.max_car_speed:
        return ScalingParameters.max_RC_PWM

    factor = (ScalingParameters.max_RC_PWM-ScalingParameters.min_RC_PWM)/ScalingParameters.max_car_speed

    scaledSpeed = speed*factor + ScalingParameters.min_RC_PWM
    
    if scaledSpeed<=ScalingParameters.min_RC_PWM:
        return 0

    return int(scaledSpeed)

    


from .ScalingParameters import ScalingParameters

# this gets a close approximate of how much the cars have travelled scaled in terms of meters
def calcDistance(pwm, interval):

    d_per_second = pwm * ScalingParameters.pwm_m_to_s / ScalingParameters.pwm_to_m

    return round(d_per_second * interval,2)

class ScalingParameters:

    # 120 km/hr is max
    max_car_speed = 120

    max_RC_PWM = 4096

    min_RC_PWM = 400

    pwm_to_m = max_RC_PWM/3.6

    km_to_m = max_car_speed/3.6

    pwm_to_car_speed = pwm_to_m/km_to_m

    pwm_m_to_s = pwm_to_car_speed/3.6

class Vars:
    # Model Parameters
    Greatest_speed_reduction = 0.5
    Zone_of_influence_upstream = 50 / 3
    Zone_of_influence_downstream = 10 / 3

    # Vehicle Parameters
    length = 1.8
    miniGap = 1.8
    initialMaxBraking = False

    # GIPPS Vehicle Parameters
    driver_reaction_time = 3 / 3
    randomness = False
    max_acceleration = 1.7
    efffective_size = length + miniGap

    # Plot parameters
    speeds = []

    # stores the recent distance travelled by the cars as sent from each car through mqtt
    over_mqtt_distances = []

    # stores the recent emergency stops made by cars and send over MQTT
    over_mqtt_emergency_stops = []

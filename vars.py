class Vars:
    # Model Parameters
    Greatest_speed_reduction = 0.5
    Zone_of_influence_upstream = 50 / 3
    Zone_of_influence_downstream = 10 / 3

    # Vehicle Parameters
    length = 20
    miniGap = 10
    initialMaxBraking = False

    # GIPPS Vehicle Parameters
    driver_reaction_time = 3 / 3
    randomness = False
    max_acceleration = 1.7
    efffective_size = length + miniGap

    # Plot parameters
    speeds = []

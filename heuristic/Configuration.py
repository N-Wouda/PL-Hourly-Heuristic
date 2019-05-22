class Configuration:
    """
    Weights and other settings for the adaptive large neighbourhood search,
    as explained on p. 9-12 in <http://orbit.dtu.dk/files/5293785/Pisinger.pdf>.
    """
    IS_BEST = 2                 # TODO fiddle with these parameters
    IS_BETTER = 1
    IS_ACCEPTED = .5
    IS_REJECTED = .1

    MAX_ITERATIONS = 10000

    INITIAL_TEMPERATURE = 500
    TEMPERATURE_DECAY = 0.99

    OPERATOR_DECAY = 0.99

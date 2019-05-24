class Configuration:
    """
    Weights and other settings for the adaptive large neighbourhood search,
    as explained on p. 9-12 in <http://orbit.dtu.dk/files/5293785/Pisinger.pdf>.
    """
    IS_BEST = 3                     # TODO fiddle with these parameters
    IS_BETTER = 1.5
    IS_ACCEPTED = .8
    IS_REJECTED = .2

    MAX_ITERATIONS = 25000

    INITIAL_TEMPERATURE = 1000
    TEMPERATURE_DECAY = 95 / 100

    OPERATOR_DECAY = 75 / 100

    FIX_SEED = False
    OUTPUT_DIAGNOSTICS = False

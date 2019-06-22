class Configuration:
    """
    Weights and other settings for the adaptive large neighbourhood search,
    as explained on p. 9-12 in <http://orbit.dtu.dk/files/5293785/Pisinger.pdf>.
    """
    IS_BEST = 3                     # TODO fiddle with these parameters
    IS_BETTER = 2
    IS_ACCEPTED = 1
    IS_REJECTED = .5

    MAX_ITERATIONS = 10000

    INITIAL_TEMPERATURE = 25000
    TEMPERATURE_DECAY = .975

    OPERATOR_DECAY = .8

    FIX_SEED = False
    OUTPUT_DIAGNOSTICS = False

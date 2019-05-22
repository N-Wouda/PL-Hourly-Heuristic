class Weights:
    """
    Weights for the adaptive large neighbourhood search, as explained on p. 12
    in <http://orbit.dtu.dk/files/5293785/Pisinger.pdf>.
    """
    IS_BEST = 2                 # TODO fiddle with these weights
    IS_BETTER = 1
    IS_ACCEPTED = .5
    IS_REJECTED = .1

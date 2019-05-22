from .State import State
from .initial_solution import initial_solution
from .operators import OPERATORS
import numpy as np
from .Configuration import Configuration


def adaptive_large_neighbourhood_search(data) -> State:
    """
    This particular implementation is largely based on the pseudo-code examples
    given at <http://orbit.dtu.dk/files/5293785/Pisinger.pdf>.
    """
    global_best = state = initial_solution(data)

    weights = np.ones_like(OPERATORS)

    for iteration in range(Configuration.MAX_ITERATIONS):
        probabilities = np.asarray(weights / weights.sum(), dtype=np.float64)

        idx = np.random.choice(len(OPERATORS), p=probabilities)
        method = OPERATORS[idx]

        next_state = method(state)

        new_objective = next_state.evaluate()
        old_objective = state.evaluate()

        if new_objective > old_objective:
            state = next_state
            weight = Configuration.IS_BETTER
        # This term is borrowed from simulated annealing, to allow for worse
        # choices in the beginning.
        elif accept(new_objective, old_objective) > np.random.random():
            state = next_state
            weight = Configuration.IS_ACCEPTED
        else:
            weight = Configuration.IS_REJECTED

        # This is already the new state, if it was better than the previous.
        if state.evaluate() > global_best.evaluate():
            global_best = state
            weight = Configuration.IS_BEST

        # Updates the weight associated with the selected method
        weights[idx] = convex_combination(Configuration.OPERATOR_DECAY,
                                          weights[idx],
                                          weight)

    return state


def accept(new, old):
    """
    Computes the acceptance probability according to a simulated annealing
    scheme. <https://en.wikipedia.org/wiki/Simulated_annealing#Pseudocode>.
    """
    return np.exp((old - new) / next(get_temperature()))


def get_temperature():
    """
    Generator method that returns the current temperature, to be used in
    determining the acceptance probability.
    """
    temperature = Configuration.INITIAL_TEMPERATURE

    while True:
        yield temperature                                           # see p. 9
        temperature = temperature * Configuration.TEMPERATURE_DECAY


def convex_combination(parameter, a, b):
    return parameter * a + (1 - parameter) * b                  # see p. 12

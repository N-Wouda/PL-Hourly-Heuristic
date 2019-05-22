from .State import State
from .initial_solution import initial_solution
from .operators import OPERATORS
import numpy as np
from .Weights import Weights


def large_neighbourhood_search(data, max_iterations: int) -> State:
    """
    This particular implementation is largely based on the pseudo-code examples
    given at <http://orbit.dtu.dk/files/5293785/Pisinger.pdf>.
    """
    state = initial_solution(data)

    weights = np.ones_like(OPERATORS)

    for iteration in range(max_iterations):
        probabilities = np.asarray(weights / weights.sum(), dtype=np.float64)

        idx = np.random.choice(len(OPERATORS), p=probabilities)
        method = OPERATORS[idx]

        next_state = method(state)

        # TODO accept or reject, and update weights

    return state

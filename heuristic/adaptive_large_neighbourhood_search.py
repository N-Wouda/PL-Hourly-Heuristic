from typing import List, Tuple

import numpy as np

from .Configuration import Configuration
from utils import Data, State
from .initial_solution import initial_solution
from .operators import OPERATORS
from .utils import accept, convex_combination


def adaptive_large_neighbourhood_search(data: Data) \
        -> Tuple[State, State, List[float], List]:
    """
    This particular implementation is largely based on the pseudo-code examples
    given at <http://orbit.dtu.dk/files/5293785/Pisinger.pdf>.

    Returns
    -------
    Tuple[State, State, List[float], List]
        In order, this includes:
            * The final solution state
            * The best observed solution
            * A history of state objective values
            * A history of probabilities associated with the available
              operators
    """
    global_best = state = initial_solution(data)
    weights = np.ones_like(OPERATORS)

    history = [state.objective()]
    weight_history = [weights / weights.sum()]

    for iteration in range(Configuration.MAX_ITERATIONS):
        probabilities = np.asarray(weights / weights.sum(), dtype=np.float64)

        idx = np.random.choice(len(OPERATORS), p=probabilities)
        method = OPERATORS[idx]

        state, weight = _update(method(state), state)

        # This is already the new state, if it was better than the previous.
        if state.objective() > global_best.objective():
            global_best = state
            weight = Configuration.IS_BEST

        history.append(state.objective())
        weight_history.append(weights / weights.sum())

        # Updates the weight associated with the selected method
        weights[idx] = convex_combination(weights[idx], weight)

    return state, global_best, history, weight_history


def _update(new: State, old: State) -> Tuple[State, float]:
    """
    Determines the next state, and the weight associated with the performed
    operation.
    """
    if new.objective() > old.objective():
        return new, Configuration.IS_BETTER
    elif new.objective() == old.objective():    # this might imply some tidying
        return new, Configuration.IS_ACCEPTED   # up, which we do want to keep.

    # This is borrowed from simulated annealing, to allow for worse choices
    # in the beginning.
    if accept(new.objective(), old.objective()) > np.random.random():
        return new, Configuration.IS_ACCEPTED
    else:
        return old, Configuration.IS_REJECTED

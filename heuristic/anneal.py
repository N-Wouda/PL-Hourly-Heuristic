from .initial_solution import initial_solution
from cmath import exp
from .State import State
from random import random
from .evaluate import evaluate


def anneal(max_iterations=10000) -> State:
    """
    This particular implementation is largely based on the pseudo-code given at
    <https://en.wikipedia.org/wiki/Simulated_annealing#Pseudocode>.
    """
    state = initial_solution()

    for iteration in range(max_iterations):
        temperature = _temperature(iteration, max_iterations)

        next_state = _neighbour(state)
        accept_probability = _acceptance(evaluate(next_state),
                                         evaluate(state),
                                         temperature)

        if accept_probability > random():
            state = next_state

    return state


def _temperature(iteration: int, max_iterations: int) -> float:
    pass


def _acceptance(new: float, old: float, temperature: float) -> float:
    if new > old:
        return 1

    return exp(-(old - new) / temperature)


def _neighbour(state: State) -> State:
    pass

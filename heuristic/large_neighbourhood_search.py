from .State import State
from .initial_solution import initial_solution


def large_neighbourhood_search(data, max_iterations: int) -> State:
    """
    This particular implementation is largely based on the pseudo-code examples
    given at <http://orbit.dtu.dk/files/5293785/Pisinger.pdf>.
    """
    state = initial_solution(data)

    for iteration in range(max_iterations):
        pass

    return state

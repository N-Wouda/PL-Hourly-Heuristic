from utils import State


def objective(state: State) -> float:
    """
    Computes the state's objective value.
    """
    return state.objective()

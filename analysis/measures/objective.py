from utils import State


def objective(state: State) -> float:
    return state.objective()

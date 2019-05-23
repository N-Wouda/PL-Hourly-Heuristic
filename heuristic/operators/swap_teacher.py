from ..State import State


def swap_teacher(state: State) -> State:
    """
    Swaps an activity teacher with one in self-study, if applicable.
    """
    return State.from_state(state)      # TODO

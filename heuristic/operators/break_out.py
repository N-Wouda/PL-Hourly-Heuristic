from ..State import State


def break_out(state: State) -> State:
    """
    Breaks-out an activity from self-study, if possible.
    """
    return State.from_state(state)      # TODO

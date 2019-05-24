from ..State import State


def split_activity(state: State) -> State:
    """
    Splits an activity in two, if applicable.
    """
    return State.from_state(state)      # TODO

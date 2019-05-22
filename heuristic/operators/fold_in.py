from ..State import State


def fold_in(state: State) -> State:
    """
    Folds-in an activity into self-study, if applicable.
    """
    return State.from_state(state)      # TODO

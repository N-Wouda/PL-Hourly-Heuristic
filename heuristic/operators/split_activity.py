from utils import State
from heuristic.utils import find_teacher, find_classroom, random_activity


def split_activity(state: State) -> State:
    """
    Splits an activity in two, if applicable.
    """
    classroom, teacher, module = random_activity(state)

    other_classroom = find_classroom(state, module)
    other_teacher = find_teacher(state, module)

    if other_teacher is not False and other_classroom is not False:
        new_state = State.from_state(state)
        new_assignment = (other_classroom, other_teacher)

        new_state.classroom_teacher_assignments[new_assignment] = module

        return new_state

    return state

from utils import State
from heuristic.utils import find_teacher, random_activity


def swap_teacher(state: State) -> State:
    """
    Swaps an activity teacher with one in self-study or unassigned,
    if applicable.
    """
    classroom, teacher, module = random_activity(state)
    other_teacher = find_teacher(state, module)

    if other_teacher is not False:
        new_state = State.from_state(state)
        new_assignment = (classroom, other_teacher)

        # Remove the old, and insert the newly swapped assignment
        del new_state.classroom_teacher_assignments[(classroom, teacher)]
        new_state.classroom_teacher_assignments[new_assignment] = module

        return new_state

    return state

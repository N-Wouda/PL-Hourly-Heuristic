from numpy.random import RandomState

from heuristic.utils import find_teacher, HeuristicState, random_activity


def swap_teacher(state: HeuristicState, rnd: RandomState) -> HeuristicState:
    """
    Swaps an activity teacher with one in self-study or unassigned,
    if applicable.
    """
    classroom, teacher, module = random_activity(state, rnd)
    other_teacher = find_teacher(state, module)

    if other_teacher is not False:
        new_state = state.copy()
        new_assignment = (classroom, other_teacher)

        # Remove the old, and insert the newly swapped assignment
        del new_state.classroom_teacher_assignments[(classroom, teacher)]
        new_state.classroom_teacher_assignments[new_assignment] = module

        return new_state

    return state

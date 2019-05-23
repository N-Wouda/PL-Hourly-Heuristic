from ..State import State
import numpy as np
from .find_teacher import find_teacher
from .find_classroom import find_classroom


def break_out(state: State) -> State:
    """
    Breaks-out an activity from self-study, if possible.
    """
    self_study_learners = state.learner_assignments == -1

    # Gets all modules that are preferred by learners currently in self study,
    # and computes those that do not yet have an activity.
    all_modules = np.unique(state.most_preferred[self_study_learners, :])
    not_assigned = set(all_modules) - state.module_assignments

    # Aggregate self-study learner preferences per module
    histogram = [(module, np.sum(state.preferences[self_study_learners,
                                                   module]))
                 for module in not_assigned]

    histogram.sort(key=lambda item: item[1])

    # Finds the first module that can be assigned, in order of descending
    # aggregate preferences.
    for module, _ in reversed(histogram):
        teacher = find_teacher(state, module)
        classroom = find_classroom(state, module)

        if not teacher or not classroom:        # no teacher or classroom is
            continue                            # available for this module

        # We have all the ingredients to host an activity with this module, so
        # we can create a new state.
        new_state = State.from_state(state)

        preferences = state.preferences[self_study_learners, module]
        learners = preferences.nonzero()

        # Check the minimum and maximum bounds
        if len(learners[0]) < state.min_batch:
            continue

        max_group_size = min(state.max_batch,
                             state.classrooms[classroom]['capacity'])

        if len(learners[0]) > max_group_size:
            # This exploits a neat trick: the indices into the preferences
            # array are the learner IDs. Since we have more learners than
            # max_group_size, we only select those learners that most prefer
            # this module assignment.
            indices = (-preferences).argsort()
            learners = indices[:max_group_size]

        # Assign all selected learners to the new module
        new_state.learner_assignments[learners] = module

        # And finally, assign the (classroom, teacher) pair
        new_state.classroom_teacher_assignments[(classroom, teacher)] = module

        return new_state

    return state        # we could not find an activity to schedule

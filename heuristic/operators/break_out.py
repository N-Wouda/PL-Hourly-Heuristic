import numpy as np

from heuristic.utils import find_classroom, find_teacher
from utils import State


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

        if teacher is False or classroom is False:  # no teacher or classroom is
            continue                                # available for this module

        # We have all the ingredients to host an activity with this module, so
        # we can create a new state.
        new_state = State.from_state(state)

        # Of these learners, we should make sure their assignment *improves*:
        # the newly selected preferences should be above what their current
        # assignment provides.
        current = state.preferences[:, -1] - state.penalty
        module_preferences = state.preferences[:, module]

        learners, *_ = np.nonzero(      # indices/IDs where these masks hold
            (self_study_learners == 1)
            & (module_preferences != 0)
            & (current < state.preferences[:, module]))

        if len(learners) < state.min_batch:         # ensures minimum bound
            continue

        learners = learners[:min(state.max_batch,   # ensures maximum bound
                                 state.classrooms[classroom]['capacity'])]

        # Assign all selected learners to the new module and (classroom,
        # teacher) pair
        new_state.learner_assignments[learners] = module
        new_state.classroom_teacher_assignments[(classroom, teacher)] = module

        return new_state

    return state        # we could not find an activity to schedule

import numpy as np
from numpy.random import RandomState

from utils import State


def swap_learner(state: State, rnd: RandomState) -> State:
    """
    Swaps two selected learners, if applicable.
    """
    learner = np.random.choice(state.learners)['id']
    preferences = state.most_preferred[learner, :]

    for module in preferences:
        # The selected learner holds a preference for this module, *and* we
        # have an activity for this module.
        if module not in state.module_assignments:
            continue

        module_learners = np.where(state.learner_assignments == module)
        current = state.learner_assignments[learner]

        # We try to find a learner in the proposed activity that can swap to
        # this learner's current activity.
        for other in module_learners[0]:
            if other == learner:                # cannot swap with self
                continue

            # Either the current activity is self-study (then any learner
            # can swap), or the other learner should hold a preference.
            if np.any(state.most_preferred[other, :] == current) \
                    or current == len(state.modules) - 1:
                new_state = state.copy()

                new_state.learner_assignments[learner] = module
                new_state.learner_assignments[other] = current

                return new_state

    return state

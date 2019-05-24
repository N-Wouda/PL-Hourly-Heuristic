import numpy as np

from utils import State
from typing import Tuple


def random_activity(state: State) -> Tuple[int, int, int]:
    """
    Returns a random activity, currently scheduled in the passed-in state.

    Returns
    -------
    Tuple[int, int, int]
        A tuple of (classroom, teacher, module).
    """
    pairs = list(state.classroom_teacher_assignments)

    # Randomly selected activity pair
    classroom, teacher = pairs[np.random.randint(0, len(pairs))]
    module = state.classroom_teacher_assignments[(classroom, teacher)]

    return classroom, teacher, module

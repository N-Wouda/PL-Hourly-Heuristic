from collections import defaultdict
from typing import List, Tuple

from src.constants import SELF_STUDY_MODULE_ID
from src.functions import get_problem


def activity_size(solution: List[Tuple]) -> bool:
    """
    Verifies each activity satisfies both the minimum and maximum group size
    constraints.
    """
    problem = get_problem()
    classroom_learners = defaultdict(set)

    for learner, module, classroom, _ in solution:
        classroom_learners[classroom, module].add(learner)

    for (classroom, module), learners in classroom_learners.items():
        max_capacity = problem.classrooms[classroom].capacity

        if module != SELF_STUDY_MODULE_ID:
            max_capacity = min(problem.max_batch, max_capacity)

        if not problem.min_batch <= len(learners) <= max_capacity:
            return False

    return True

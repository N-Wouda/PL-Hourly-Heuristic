from collections import defaultdict
from typing import List, Tuple

from utils import Data, max_capacity


def activity_size(data: Data, solution: List[Tuple]) -> bool:
    """
    Verifies each activity satisfies both the minimum and maximum group size
    constraints.
    """
    classroom_learners = defaultdict(set)

    for assignment in solution:
        learner, module, classroom, _ = assignment
        classroom_learners[classroom, module].add(learner)

    return all(data.min_batch
               <= len(learners)
               <= max_capacity(data.max_batch,
                               data.classrooms[classroom]["capacity"],
                               module == len(data.modules) - 1)
               for (classroom, module), learners in classroom_learners.items())

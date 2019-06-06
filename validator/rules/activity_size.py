from collections import defaultdict
from typing import List, Tuple

from utils import Data


def activity_size(data: Data, solution: List[Tuple]) -> bool:
    """
    Verifies each activity satisfies both the minimum and maximum group size
    constraints.
    """
    classroom_learners = defaultdict(set)

    for assignment in solution:
        learner, _, classroom, _ = assignment
        classroom_learners[classroom].add(learner)

    # TODO max batch size for non self-study (how?)
    return all(data.min_batch
               <= len(learners)
               <= data.classrooms[classroom]["capacity"]
               for classroom, learners in classroom_learners.items())

from typing import List, Tuple

from utils import Data
from collections import defaultdict


def learners_to_modules(data: Data, solution: List[Tuple]) -> bool:
    """
    Verifies each learner is assigned to *one* module, and all learners are
    assigned.
    """
    learner_modules = defaultdict(set)

    for assignment in solution:
        learner, module, *_ = assignment
        learner_modules[learner].add(module)

    return all(len(value) == 1 for value in learner_modules.values()) \
        and len(learner_modules) == len(data.learners)

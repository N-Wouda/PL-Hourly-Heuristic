from collections import defaultdict
from typing import List, Tuple

from heuristic.classes import Problem


def learners_to_modules(solution: List[Tuple]) -> bool:
    """
    Verifies each learner is assigned to *one* module, and all learners are
    assigned.
    """
    problem = Problem()
    learner_modules = defaultdict(set)

    for assignment in solution:
        learner, module, *_ = assignment
        learner_modules[learner].add(module)

    if len(learner_modules) != problem.num_learners:
        return False

    return all(len(value) == 1 for value in learner_modules.values())

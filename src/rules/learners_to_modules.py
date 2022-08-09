from collections import defaultdict
from typing import List, Tuple


def learners_to_modules(problem, solution: List[Tuple]) -> bool:
    """
    Verifies each learner is assigned to *one* module, and all learners are
    assigned.
    """
    learner_modules = defaultdict(set)

    for learner, module, *_ in solution:
        learner_modules[learner].add(module)

    if len(learner_modules) != problem.num_learners:
        return False

    return all(len(value) == 1 for value in learner_modules.values())

from collections import defaultdict
from typing import List, Tuple


def teachers_to_modules(solution: List[Tuple]) -> bool:
    """
    Verifies each teacher is assigned to *one* module.
    """
    teacher_modules = defaultdict(set)

    for assignment in solution:
        _, module, _, teacher = assignment
        teacher_modules[teacher].add(module)

    return all(len(value) == 1 for value in teacher_modules.values())

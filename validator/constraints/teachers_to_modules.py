from collections import defaultdict
from typing import List, Tuple

from utils import Data


def teachers_to_modules(data: Data, solution: List[Tuple]) -> bool:
    """
    Verifies each teacher is assigned to *one* module.
    """
    teacher_modules = defaultdict(lambda: set())

    for assignment in solution:
        _, module, _, teacher = assignment
        teacher_modules[teacher].add(module)

    return all(len(value) == 1
               for value in teacher_modules.values())

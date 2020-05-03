from collections import defaultdict
from typing import List, Tuple

from heuristic.classes import Problem


def classrooms_to_modules(solution: List[Tuple]) -> bool:
    """
    Verifies the number of classrooms assigned is less than the total number
    of classrooms available, and each classroom is assigned to *one* module
    only.
    """
    problem = Problem()
    classroom_modules = defaultdict(set)

    for assignment in solution:
        _, module, classroom, _ = assignment
        classroom_modules[classroom].add(module)

    if len(classroom_modules) > len(problem.classrooms):
        return False

    return all(len(value) == 1 for value in classroom_modules.values())

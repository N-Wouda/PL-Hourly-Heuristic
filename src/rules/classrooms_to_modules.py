from collections import defaultdict
from typing import List, Tuple


def classrooms_to_modules(problem, solution: List[Tuple]) -> bool:
    """
    Verifies the number of classrooms assigned is less than the total number
    of classrooms available, and each classroom is assigned to *one* module
    only.
    """
    classroom_modules = defaultdict(set)

    for _, module, classroom, _ in solution:
        classroom_modules[classroom].add(module)

    if len(classroom_modules) > len(problem.classrooms):
        return False

    return all(len(value) == 1 for value in classroom_modules.values())

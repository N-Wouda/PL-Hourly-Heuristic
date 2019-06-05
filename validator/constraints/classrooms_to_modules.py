from collections import defaultdict
from typing import List, Tuple

from utils import Data


def classrooms_to_modules(data: Data, solution: List[Tuple]) -> bool:
    """
    Verifies the number of classrooms assigned is less than the total number
    of classrooms available, and each classroom is assigned to *one* module
    only.
    """
    classroom_modules = defaultdict(set)

    for assignment in solution:
        _, module, classroom, _ = assignment
        classroom_modules[classroom].add(module)

    return all(len(value) == 1 for value in classroom_modules.values()) \
        and len(classroom_modules) <= len(data.classrooms)

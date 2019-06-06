from collections import defaultdict
from typing import List, Tuple

from utils import Data


def classroom_teacher_tuples_to_modules(data: Data,
                                        solution: List[Tuple]) -> bool:
    """
    Verifies each (classroom, teacher) tuple is assigned to *one* module.
    """
    classroom_teacher_module = defaultdict(set)

    for assignment in solution:
        _, module, classroom, teacher = assignment
        classroom_teacher_module[classroom, teacher].add(module)

    return all(len(value) == 1
               for value in classroom_teacher_module.values())

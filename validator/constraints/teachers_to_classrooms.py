from collections import defaultdict
from typing import List, Tuple

from utils import Data


def teachers_to_classrooms(data: Data, solution: List[Tuple]) -> bool:
    """
    Verifies each teacher is assigned to *one* classroom, and at most all
    teachers are in use.
    """
    teacher_classrooms = defaultdict(lambda: set())

    for assignment in solution:
        *_, classroom, teacher = assignment
        teacher_classrooms[teacher].add(classroom)

    return all(len(value) == 1 for value in teacher_classrooms.values()) \
        and len(teacher_classrooms) <= len(data.teachers)

from collections import defaultdict
from typing import List, Tuple

from src.classes import Problem


def teachers_to_classrooms(solution: List[Tuple]) -> bool:
    """
    Verifies each teacher is assigned to *one* classroom, and at most all
    teachers are in use.
    """
    problem = Problem()
    teacher_classrooms = defaultdict(set)

    for assignment in solution:
        *_, classroom, teacher = assignment
        teacher_classrooms[teacher].add(classroom)

    if len(teacher_classrooms) > len(problem.teachers):
        return False

    return all(len(value) == 1 for value in teacher_classrooms.values())

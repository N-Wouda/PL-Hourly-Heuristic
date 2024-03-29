from collections import defaultdict
from typing import List, Tuple


def teachers_to_classrooms(problem, solution: List[Tuple]) -> bool:
    """
    Verifies each teacher is assigned to *one* classroom, and at most all
    teachers are in use.
    """
    teacher_classrooms = defaultdict(set)

    for *_, classroom, teacher in solution:
        teacher_classrooms[teacher].add(classroom)

    if len(teacher_classrooms) > len(problem.teachers):
        return False

    return all(len(value) == 1 for value in teacher_classrooms.values())

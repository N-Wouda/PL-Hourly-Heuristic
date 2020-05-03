from collections import defaultdict
from typing import List, Tuple

from heuristic.classes import Problem


def classrooms_to_teachers(solution: List[Tuple]) -> bool:
    """
    Verifies each classroom is assigned to only *one* teacher.
    """
    problem = Problem()
    classroom_teachers = defaultdict(set)

    for assignment in solution:
        *_, classroom, teacher = assignment
        classroom_teachers[classroom].add(teacher)

    if len(classroom_teachers) > len(problem.classrooms):
        return False

    return all(len(value) == 1 for value in classroom_teachers.values())

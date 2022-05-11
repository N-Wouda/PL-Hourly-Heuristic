from collections import defaultdict
from typing import List, Tuple

from src.functions import get_problem


def classrooms_to_teachers(solution: List[Tuple]) -> bool:
    """
    Verifies each classroom is assigned to only *one* teacher.
    """
    problem = get_problem()
    classroom_teachers = defaultdict(set)

    for *_, classroom, teacher in solution:
        classroom_teachers[classroom].add(teacher)

    if len(classroom_teachers) > len(problem.classrooms):
        return False

    return all(len(value) == 1 for value in classroom_teachers.values())

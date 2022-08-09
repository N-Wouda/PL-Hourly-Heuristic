from collections import defaultdict
from typing import List, Tuple


def classrooms_to_teachers(problem, solution: List[Tuple]) -> bool:
    """
    Verifies each classroom is assigned to only *one* teacher.
    """
    classroom_teachers = defaultdict(set)

    for *_, classroom, teacher in solution:
        classroom_teachers[classroom].add(teacher)

    if len(classroom_teachers) > len(problem.classrooms):
        return False

    return all(len(value) == 1 for value in classroom_teachers.values())

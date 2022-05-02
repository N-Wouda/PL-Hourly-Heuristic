from typing import List, Tuple

from src.functions import get_problem


def module_classroom_room_type(solution: List[Tuple]) -> bool:
    """
    Verifies each classroom-module assignment satisfies the room type
    requirement.
    """
    problem = get_problem()
    classrooms = {}

    for _, module, classroom, _ in solution:
        classrooms[classroom] = module

    for classroom_idx, module_idx in classrooms.items():
        classroom = problem.classrooms[classroom_idx]
        module = problem.modules[module_idx]

        if not classroom.is_qualified_for(module):
            return False

    return True

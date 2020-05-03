from typing import List, Tuple

from heuristic.classes import Problem


def module_classroom_room_type(solution: List[Tuple]) -> bool:
    """
    Verifies each classroom-module assignment satisfies the room type
    requirement.
    """
    problem = Problem()
    classrooms = {}

    for assignment in solution:
        _, module, classroom, _ = assignment
        classrooms[classroom] = module

    for classroom_idx, module_idx in classrooms.items():
        classroom = problem.classrooms[classroom_idx]
        module = problem.modules[module_idx]

        if not classroom.is_qualified_for(module):
            return False

    return True

from typing import List, Tuple


def module_classroom_room_type(problem, solution: List[Tuple]) -> bool:
    """
    Verifies each classroom-module assignment satisfies the room type
    requirement.
    """
    classrooms = {}

    for _, module, classroom, _ in solution:
        classrooms[classroom] = module

    for classroom_idx, module_idx in classrooms.items():
        classroom = problem.classrooms[classroom_idx]
        module = problem.modules[module_idx]

        if not classroom.is_qualified_for(module):
            return False

    return True

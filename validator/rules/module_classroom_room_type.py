from typing import List, Tuple

from utils import Data


def module_classroom_room_type(data: Data, solution: List[Tuple]) -> bool:
    """
    Verifies each classroom-module assignment satisfies the room type
    requirement.
    """
    classrooms = {}

    for assignment in solution:
        _, module, classroom, _ = assignment
        classrooms[classroom] = module

    return all(_is_allowed(data.classrooms[classroom], data.modules[module])
               for classroom, module in classrooms.items())


def _is_allowed(classroom, module) -> bool:
    if module["id"] == -1:      # self study, so is that allowed in this room?
        return classroom["self_study_allowed"]

    return classroom["room_type"] == module["room_type"]

from typing import Union
from heuristic.State import State


def find_teacher(state: State, module: int) -> Union[int, bool]:
    # Gets all teachers that are not currently in use.
    teachers = set(range(len(state.teachers))) - state.teacher_assignments
    qualification_needed = state.modules[module]['qualification']

    # Finds the first teacher that fits the required qualification, if any.
    for teacher in teachers:
        if state.qualifications[teacher, module] <= qualification_needed:
            return teacher

    return False

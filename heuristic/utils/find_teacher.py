from typing import Union
from utils import State


def find_teacher(state: State, module: int) -> Union[int, bool]:
    """
    Finds a teacher that can teach the passed-in module. If none exist, this
    function returns False, else an integer is returned (the teacher ID).
    """
    qualification_needed = state.modules[module]['qualification']

    # Gets all teachers that are not currently in use.
    teachers = set(range(len(state.teachers))) - state.teacher_assignments

    if module == -1 and len(teachers):  # since self-study does not actually
        return next(iter(teachers))     # require any specific qualification

    teachers = [                            # finds the first teacher that fits
        teacher for teacher in teachers     # the required qualification
        if 0 < state.qualifications[teacher, module] <= qualification_needed]

    if not len(teachers):
        return False

    # Finds a teacher that meets the requirements with minimal overhead.
    return min(teachers,
               key=lambda teacher: state.qualifications[teacher, module])

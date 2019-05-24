from typing import Union
from utils import State


def find_classroom(state: State, module: int) -> Union[int, bool]:
    """
    Finds a classroom that can host the passed-in module. If none exist, this
    function returns False, else an integer is returned (the classroom ID).
    """
    room_type_needed = state.modules[module]['room_type']

    # Gets all classrooms that are not currently in use.
    classrooms = set(range(len(state.classrooms))) - state.classroom_assignments

    # Finds the first classroom that fits the required room type, if any.
    for classroom in classrooms:
        if state.classrooms[classroom]['room_type'] == room_type_needed:
            return classroom

        # Since self-study is generally allowed in multiple room types.
        if module == -1 and state.classrooms[classroom]['self_study_allowed']:
            return classroom

    return False

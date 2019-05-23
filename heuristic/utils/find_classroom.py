from typing import Union
from heuristic.State import State


def find_classroom(state: State, module: int) -> Union[int, bool]:
    # Gets all classrooms that are not currently in use.
    classrooms = set(range(len(state.classrooms))) - state.classroom_assignments
    room_type_needed = state.modules[module]['room_type']

    # Finds the first classroom that fits the required room type, if any.
    for classroom in classrooms:
        if state.classrooms[classroom]['room_type'] == room_type_needed:
            return classroom

    return False

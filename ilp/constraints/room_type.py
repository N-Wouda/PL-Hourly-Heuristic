import itertools

from utils import Data


def room_type(data: Data, solver):
    """
    For each classroom-module assignment, this guarantees the room types agree.
    Room types are categorical ({1, 2, ...}), where only equality suffices -
    there is no ordering!

    Note
    ----
    This constraint does not hold for self-study; self-study is checked in the
    ``self_study_allowed`` constraint.
    """
    for module, classroom in itertools.product(range(len(data.modules) - 1),
                                               range(len(data.classrooms))):
        classroom_module = solver.sum(
            solver.module_resources[module, classroom, teacher]
            for teacher in range(len(data.teachers)))

        module_room_type = data.modules[module]["room_type"]
        classroom_room_type = data.classrooms[classroom]["room_type"]

        # Room type is a categorical variable: the only requirement is that,
        # if the classroom is assigned to the given module, that the room types
        # match *exactly*.
        solver.add_constraint(module_room_type * classroom_module
                              == classroom_room_type * classroom_module)

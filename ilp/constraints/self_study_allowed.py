from utils import Data


def self_study_allowed(data: Data, solver):
    """
    For each classroom, checks if a self-study assignment is allowed. This
    ensures only classrooms that allow self-study are used for self-study
    assignments.

    Note
    ----
    Multiple room types allow self-study, so self-study has its own boolean
    flag to differentiate.
    """
    for classroom in range(len(data.classrooms)):
        assignment = solver.sum(
            solver.module_resources[len(data.modules) - 1, classroom, teacher]
            for teacher in range(len(data.teachers)))

        classroom_self_study = data.classrooms[classroom]["self_study_allowed"]

        solver.add_constraint(assignment <= int(classroom_self_study))

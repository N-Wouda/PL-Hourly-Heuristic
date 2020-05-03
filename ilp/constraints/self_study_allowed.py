from heuristic.classes import Problem


def self_study_allowed(solver):
    """
    For each classroom, checks if a self-study assignment is allowed. This
    ensures only classrooms that allow self-study are used for self-study
    assignments.

    Note
    ----
    Multiple room types allow self-study, so self-study has its own boolean
    flag to differentiate.
    """
    problem = Problem()

    for classroom in range(len(problem.classrooms)):
        assignment = solver.sum(
            solver.module_resources[len(problem.modules) - 1,
                                    classroom,
                                    teacher]
            for teacher in range(len(problem.teachers)))

        is_allowed = problem.classrooms[classroom].is_self_study_allowed()
        solver.add_constraint(assignment <= is_allowed)

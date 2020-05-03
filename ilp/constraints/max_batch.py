from heuristic.classes import Classroom, Module, Problem


def max_batch(solver):
    """
    This constraints guarantees the number of learners assigned to a module
    are supported by a sufficient number of classroom-teacher activities, such
    that the maximum batch and capacity constraints are satisfied.

    Note
    ----
    The ``max_batch`` constraint only holds for regular instruction activities,
    for self-study the constraint defaults to a capacity requirement.
    """
    problem = Problem()

    for module in problem.modules:
        module_learners = solver.sum(solver.assignment[learner.id, module.id]
                                     for learner in problem.learners)

        activities = solver.sum(
            solver.module_resources[module.id, classroom.id, teacher.id]
            * _max_capacity(classroom, module)
            for classroom in problem.classrooms
            for teacher in problem.teachers)

        solver.add_constraint(module_learners <= activities)


def _max_capacity(classroom: Classroom, module: Module) -> int:
    """
    Computes the maximum room capacity, subject to constraints.
    """
    if module.is_self_study():
        return classroom.capacity

    return min(classroom.capacity, Problem().max_batch)

from utils import Data, max_capacity


def max_batch(data: Data, solver):
    """
    This constraints guarantees the number of learners assigned to a module
    are supported by a sufficient number of classroom-teacher activities, such
    that the maximum batch and capacity constraints are satisfied.

    Note
    ----
    The ``max_batch`` constraint only holds for regular instruction activities,
    for self-study the constraint defaults to a capacity requirement.
    """
    for module in range(len(data.modules)):
        module_learners = solver.sum(solver.assignment[learner, module]
                                     for learner in range(len(data.learners)))

        activities = solver.sum(
            solver.module_resources[module, classroom, teacher] * max_capacity(
                data.classrooms[classroom]["capacity"],
                data.max_batch,
                module == len(data.modules) - 1)
            for classroom in range(len(data.classrooms))
            for teacher in range(len(data.teachers)))

        solver.add_constraint(module_learners <= activities)

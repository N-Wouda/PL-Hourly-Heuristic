from utils import Data


def min_batch(data: Data, solver):
    """
    This constraints guarantees the number of learners assigned to a module
    are supported by a sufficient number of classroom-teacher activities, such
    that the minimum batch constraint is satisfied. This constraint holds for
    both instruction and self-study activities.
    """
    for module in range(len(data.modules)):
        module_learners = solver.sum(solver.assignment[learner, module]
                                     for learner in range(len(data.learners)))

        activities = solver.sum(
            solver.module_resources[module, classroom, teacher]
            for classroom in range(len(data.classrooms))
            for teacher in range(len(data.teachers)))

        solver.add_constraint(module_learners >= data.min_batch * activities)

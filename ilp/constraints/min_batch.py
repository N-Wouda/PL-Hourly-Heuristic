from heuristic.classes import Problem


def min_batch(solver):
    """
    This constraints guarantees the number of learners assigned to a module
    are supported by a sufficient number of classroom-teacher activities, such
    that the minimum batch constraint is satisfied. This constraint holds for
    both instruction and self-study activities.
    """
    problem = Problem()

    for module in range(len(problem.modules)):
        module_learners = solver.sum(solver.assignment[learner, module]
                                     for learner in range(problem.num_learners))

        activities = solver.sum(
            solver.module_resources[module, classroom, teacher]
            for classroom in range(len(problem.classrooms))
            for teacher in range(len(problem.teachers)))

        solver.add_constraint(module_learners >= problem.min_batch * activities)

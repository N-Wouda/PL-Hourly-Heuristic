from heuristic.classes import Problem


def learner_schedule(solver):
    """
    This constraint ensures learners are assigned to exact *one* module.
    """
    problem = Problem()

    for learner in range(problem.num_learners):
        assignments = solver.sum(solver.assignment[learner, module]
                                 for module in range(len(problem.modules)))

        solver.add_constraint(assignments == 1)

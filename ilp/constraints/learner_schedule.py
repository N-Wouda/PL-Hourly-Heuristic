from utils import Data


def learner_schedule(data: Data, solver):
    """
    This constraint ensures learners are assigned to exact *one* module.
    """
    for learner in range(len(data.learners)):
        assignments = solver.sum(solver.assignment[learner, module]
                                 for module in range(len(data.modules)))

        solver.add_constraint(assignments == 1)

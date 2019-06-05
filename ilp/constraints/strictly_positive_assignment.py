import itertools

from utils import Data


def strictly_positive_assignment(data: Data, solver):
    for i, j in itertools.product(range(len(data.learners)),
                                  range(len(data.modules))):
        assignment_pref = data.preferences[i, j] * solver.assignment[i, j]
        grace_term = solver.B * (1 - solver.assignment[i, j])

        # Eq. (18)
        solver.add_constraint(assignment_pref + grace_term >= 0.00001)

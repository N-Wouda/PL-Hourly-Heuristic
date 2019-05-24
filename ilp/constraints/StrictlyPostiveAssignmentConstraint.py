from .BaseConstraint import BaseConstraint
import itertools


class StrictlyPositiveAssignmentConstraint(BaseConstraint):

    @staticmethod
    def apply(solver, data):
        for i, j in itertools.product(range(len(data["learners"])),
                                      range(len(data["modules"]))):

            assignment_pref = solver.P[i, j] * solver.assignment[i, j]
            grace_term = solver.B * (1 - solver.assignment[i, j])

            solver.add_constraint(
                assignment_pref + grace_term >= 0.00001)  # eq. (18)

from .BaseConstraint import BaseConstraint
import itertools


class TeachingQualificationConstraint(BaseConstraint):

    @staticmethod
    def apply(solver, data):
        for j, l in itertools.product(range(len(data["modules"]) - 1),
                                      range(len(data["teachers"]))):

            assignment = solver.sum(solver.module_resources[j, k, l]
                                    for k in range(len(data["classrooms"])))

            q_m = data["modules"][j]["qualification"]

            # Eq. (16)
            solver.add_constraint((q_m - solver.Q[l, j]) * assignment >= 0)
            solver.add_constraint(solver.Q[l, j] * assignment >= 0.5)

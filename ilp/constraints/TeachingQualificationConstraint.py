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

            # Module requirement must be 'less' than teacher qualification.
            # E.g. module needs 2, then teacher can be qualified as either 1
            # or 2, but *not* 3.
            solver.add_constraint((q_m - solver.Q[l, j]) * assignment >= 0)

            # That is, greater than zero (the qualifications are {0, 1, 2, 3})
            solver.add_constraint(solver.Q[l, j] * assignment >= 0.5)

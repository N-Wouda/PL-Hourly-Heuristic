from .BaseConstraint import BaseConstraint


class LearnerScheduleConflict(BaseConstraint):

    @staticmethod
    def apply(solver, data):
        for i in range(len(data["learners"])):
            assignment = solver.sum(solver.assignment[i, j]
                                    for j in range(len(data["modules"])))

            solver.add_constraint(assignment == 1)

from .BaseConstraint import BaseConstraint


class MinBatchConstraint(BaseConstraint):

    @staticmethod
    def apply(solver, data):
        for j in range(len(data["modules"])):
            assignment = solver.sum(solver.assignment[i, j]
                                    for i in range(len(data["learners"])))

            resources_assigned = solver.sum(
                solver.module_resources[j, k, l]
                for k in range(len(data["classrooms"]))
                for l in range(len(data["teachers"])))

            solver.add_constraint(
                assignment >= solver.delta_min * resources_assigned)

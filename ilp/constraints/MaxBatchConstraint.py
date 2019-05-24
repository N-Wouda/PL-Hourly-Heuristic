from .BaseConstraint import BaseConstraint


class MaxBatchConstraint(BaseConstraint):

    @staticmethod
    def apply(solver, data):
        for j in range(len(data["modules"])):
            assignment = solver.sum(solver.assignment[i, j]
                                    for i in range(len(data["learners"])))

            resources_assigned = solver.sum(
                MaxBatchConstraint._get_size(solver.delta_max,
                                             data["classrooms"][k]["capacity"],
                                             j == len(data["modules"]) - 1)
                * solver.module_resources[j, k, l]
                for k in range(len(data["classrooms"]))
                for l in range(len(data["teachers"])))

            solver.add_constraint(assignment <= resources_assigned)

    @staticmethod
    def _get_size(delta_max, capacity, is_self_study):
        if is_self_study:
            return capacity

        return min(delta_max, capacity)

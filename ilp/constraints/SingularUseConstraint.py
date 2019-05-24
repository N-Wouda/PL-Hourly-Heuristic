from .BaseConstraint import BaseConstraint


class SingularUseConstraint(BaseConstraint):

    @staticmethod
    def apply(solver, data):
        for l in range(len(data["teachers"])):
            classroom_sum = solver.sum(solver.module_resources[j, k, l]
                                       for j in range(len(data["modules"]))
                                       for k in range(len(data["classrooms"])))

            solver.add_constraint(classroom_sum <= 1)  # eq. (9)

        for k in range(len(data["classrooms"])):
            teacher_sum = solver.sum(solver.module_resources[j, k, l]
                                     for j in range(len(data["modules"]))
                                     for l in range(len(data["teachers"])))

            solver.add_constraint(teacher_sum <= 1)  # eq. (10)

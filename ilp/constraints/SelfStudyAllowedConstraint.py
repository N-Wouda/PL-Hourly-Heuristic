from .BaseConstraint import BaseConstraint


class SelfStudyAllowedConstraint(BaseConstraint):

    @staticmethod
    def apply(solver, data):
        self_study = len(data["modules"]) - 1

        for k in range(len(data["classrooms"])):
            assignment = solver.sum(solver.module_resources[self_study, k, l]
                                    for l in range(len(data["teachers"])))

            solver.add_constraint(
                assignment <= int(data["classrooms"][k]["self_study_allowed"]))

from utils import Data


def min_batch(data: Data, solver):
    for j in range(len(data.modules)):
        assignment = solver.sum(solver.assignment[i, j]
                                for i in range(len(data.learners)))

        resources_assigned = solver.sum(
            solver.module_resources[j, k, l]
            for k in range(len(data.classrooms))
            for l in range(len(data.teachers)))

        solver.add_constraint(assignment
                              >= data.min_batch * resources_assigned)

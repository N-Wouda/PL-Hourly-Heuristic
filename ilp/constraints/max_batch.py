from utils import Data


def max_batch(data: Data, solver):
    for j in range(len(data.modules)):
        assignment = solver.sum(solver.assignment[i, j]
                                for i in range(len(data.learners)))

        resources_assigned = solver.sum(
            solver.module_resources[j, k, l] * _get_size(data.max_batch,
                                                         data.classrooms[k]["capacity"],
                                                         j == len(data.modules) - 1)
            for k in range(len(data.classrooms))
            for l in range(len(data.teachers)))

        solver.add_constraint(assignment <= resources_assigned)


def _get_size(delta_max, capacity, is_self_study):
    if is_self_study:
        return capacity

    return min(delta_max, capacity)

from heuristic.classes import Solution


def num_classrooms_used(solution: Solution):
    return len(solution.activities)

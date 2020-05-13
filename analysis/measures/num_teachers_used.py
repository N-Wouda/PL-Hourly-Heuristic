from heuristic.classes import Solution


def num_teachers_used(solution: Solution):
    return len(solution.activities)

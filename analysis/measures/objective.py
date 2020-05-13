from heuristic.classes import Solution


def objective(solution: Solution):
    return -solution.objective()

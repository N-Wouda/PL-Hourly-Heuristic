from heuristic.classes import Solution


def objective(solution: Solution) -> float:
    """
    Computes the objective value.
    """
    return -solution.objective()

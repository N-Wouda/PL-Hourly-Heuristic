from heuristic.classes import Problem, Solution


def teacher_utilisation(solution: Solution) -> float:
    """
    Computes the percentage of teachers in use from the available teacher pool.
    """
    problem = Problem()

    return 100 * len(solution.activities) / len(problem.teachers)

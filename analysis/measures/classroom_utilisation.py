from heuristic.classes import Problem, Solution


def classroom_utilisation(solution: Solution) -> float:
    """
    Computes the percentage of classrooms in use from the available classroom
    pool.
    """
    problem = Problem()

    return 100 * len(solution.activities) / len(problem.classrooms)

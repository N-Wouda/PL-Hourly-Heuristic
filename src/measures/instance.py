from src.functions import get_problem


def instance(_):
    problem = get_problem()
    return problem.instance

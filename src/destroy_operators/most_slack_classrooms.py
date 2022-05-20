from numpy.random import Generator

from src.classes import Problem, Solution


def most_slack_classrooms(current: Solution,
                          generator: Generator,
                          problem: Problem) -> Solution:
    """
    Removes activities where classrooms are underutilised (based on #learners
    / capacity, or something similar).

    TODO rewrite comment
    """
    return current

from numpy.random import Generator

from src.classes import Problem, Solution


def most_mobile_teachers(current: Solution,
                         generator: Generator,
                         problem: Problem) -> Solution:
    """
    Removes activities with teachers that can be used to teach the most
    demanded activities that are not currently scheduled (or not scheduled
    enough). This should improve the solution by making the appropriate
    resources available for a better schedule.
    """
    return current

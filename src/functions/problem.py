from src.classes import Problem

_INSTANCE = None


def get_problem() -> Problem:
    assert _INSTANCE is not None, "Problem instance not set."
    return _INSTANCE


def set_problem(problem: Problem):
    global _INSTANCE
    _INSTANCE = problem

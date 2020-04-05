from utils import State
from typing import List


class HeuristicState(State):
    """
    Wrapper to conform the State object to a minimisation objective.
    """
    unassigned = List[int]

    def objective(self):
        # The ALNS algorithm solves a minimisation objective by default, but
        # the problem is actually a maximisation problem, hence this trick.
        return -super().objective()

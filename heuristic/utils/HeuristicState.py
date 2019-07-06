from utils import State


class HeuristicState(State):
    """
    Wrapper to conform the State object to a minimisation objective.
    """

    def copy(self):
        """
        Returns a copy of the current state.
        """
        return HeuristicState(self._data,
                              self.learner_assignments.copy(),
                              self.classroom_teacher_assignments.copy())

    def objective(self):
        # The ALNS algorithm solves a minimisation objective by default, but
        # the problem is actually a maximisation problem, hence this trick.
        return -super().objective()

from utils import State


class HeuristicState(State):
    """
    Wrapper to conform the State object to a minimisation objective.
    """

    def copy(self):
        return HeuristicState(self._data,
                              self.learner_assignments.copy(),
                              self.classroom_teacher_assignments.copy())

    def objective(self):
        return -super().objective()

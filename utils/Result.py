from collections import defaultdict
from typing import List

from .State import State


class Result:

    def __init__(self, state: State):
        self._state = state

    @property
    def state(self):
        return self._state

    @property
    def assignments(self) -> List[str]:
        """
        Returns the assignments, as a list of (learner, module, classroom,
        teacher)-strings.
        """
        assignments = []
        counters = defaultdict(lambda: 0)

        for module in range(len(self.state.modules)):
            # Select learners and activities belonging to each module, such
            # that we can assign them below.
            learners = [learner for learner in range(len(self.state.learners))
                        if self.state.learner_assignments[learner] == module]

            activities = [activity for activity, activity_module
                          in self.state.classroom_teacher_assignments.items()
                          if module == activity_module]

            # Assign at least min_batch number of learners to each activity.
            # This ensures the minimum constraint is met for all activities.
            for classroom, teacher in activities:
                for _ in range(self.state.min_batch):
                    if not learners:
                        break

                    assignment = (learners.pop(), module, classroom, teacher)
                    assignments.append(str(assignment))

                    counters[classroom] += 1

            # Next we flood-fill these activities with learners, until none
            # remain to be assigned.
            for classroom, teacher in activities:
                max_capacity = min(self.state.max_batch,
                                   self.state.classrooms[classroom]['capacity'])

                if module == len(self.state.modules) - 1:  # self-study
                    max_capacity = self.state.classrooms[classroom]['capacity']

                while learners:
                    if counters[classroom] == max_capacity:
                        break

                    assignment = (learners.pop(), module, classroom, teacher)
                    assignments.append(str(assignment))

                    counters[classroom] += 1

        return assignments

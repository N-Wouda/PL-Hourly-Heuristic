from dataclasses import dataclass


@dataclass(frozen=True)
class Learner:
    id: int
    year: int

    def self_study_objective(self) -> float:
        """
        Objective value if this learner were assigned to self-study, that is,
        the maximum preference minus the self-study penalty.
        """
        from .Problem import Problem
        problem = Problem()

        module = problem.most_preferred[self.id, 0]
        return problem.preferences[self.id, module] - problem.penalty

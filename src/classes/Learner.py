from dataclasses import dataclass
from functools import lru_cache

from .Module import Module


@dataclass(frozen=True)
class Learner:
    id: int
    year: int

    @lru_cache(None)
    def is_qualified_for(self, module: Module) -> bool:
        """
        Tests if the learner is eligible to take the passed-in module.
        """
        from .Problem import Problem
        problem = Problem()

        return problem.preferences[self.id, module.id] > 0

    @lru_cache(None)
    def prefers_over_self_study(self, module: Module) -> bool:
        """
        Tests if this learner prefers the passed-in module over the
        self-study assignment (when comparing objectives).
        """
        from .Problem import Problem
        problem = Problem()

        self_study_mod = problem.most_preferred[self.id, 0]

        self_study_pref = problem.preferences[self.id, self_study_mod]
        self_study_pref -= problem.penalty

        return problem.preferences[self.id, module.id] > self_study_pref

from dataclasses import dataclass
from functools import lru_cache

from .Module import Module


@dataclass(frozen=True)
class Learner:
    id: int
    year: int

    @lru_cache(None)
    def prefers_over_self_study(self, module: Module) -> bool:
        """
        Tests if this learner prefers the passed-in module over the
        self-study assignment (when comparing objectives).
        """
        from src.functions import get_problem
        problem = get_problem()

        self_study_mod = problem.self_study_module
        self_study_pref = problem.preferences[self.id, self_study_mod.id]

        return problem.preferences[self.id, module.id] > self_study_pref

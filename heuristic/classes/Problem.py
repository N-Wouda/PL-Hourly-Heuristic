from __future__ import annotations

from collections import defaultdict
from functools import lru_cache
from typing import Any, Dict, List

import numpy as np
import simplejson as json

from heuristic.constants import SELF_STUDY_MODULE_ID
from .Classroom import Classroom
from .Learner import Learner
from .Module import Module
from .Singleton import Singleton
from .Teacher import Teacher


class Problem(metaclass=Singleton):
    _data: Dict[str, Any]

    @classmethod
    def from_instance(cls, experiment: int, instance: int) -> Problem:
        """
        Builds a Data object for the experiment data file associated with the
        given experiment and instance.
        """
        cls.clear()

        with open(f"experiments/{experiment}/{instance}.json") as file:
            data = json.load(file)

        problem = cls()
        problem._data = data

        return problem

    @property
    @lru_cache(1)
    def num_learners(self) -> int:
        return len(self._data['learners'])

    @property
    @lru_cache(1)
    def num_courses(self) -> int:
        """
        There are 48 modules per course, excluding the self-study module.
        """
        return (len(self.modules) - 1) // 48

    @property
    @lru_cache(1)
    def preferences(self) -> np.ndarray:
        """
        Learner preferences, as a NumPy array. Preferences as a matrix of
        learners (rows) to modules (column), where each element represents the
        preference of the given learner for the given module. When a preference
        is zero, the learner is ineligible to take given module.
        """
        preferences = np.asarray(self._data["preferences"])

        # Preferences, and the self-study module preference. The self-study
        # preference is given as the maximum preference held for any module
        # by the learner, as the learner will work on his/her own - presumably
        # on the most preferred module.
        return np.concatenate((preferences, np.max(preferences, 1)[:, None]), 1)

    @property
    @lru_cache(1)
    def most_preferred(self):
        """
        Returns the most preferred module (index/ID) per learner.
        """
        by_module = np.argsort(-self.preferences[:, :-1], axis=1)

        # Since only one module per course may be preferred, we can safely
        # discard all the others.
        return by_module[:, :self.num_courses]

    @property
    @lru_cache(1)
    def prefers_over_self_study(self) -> Dict[Learner, List[Module]]:
        """
        Returns a dictionary with modules, per learner, that are preferred
        over the self-study assignment.
        """
        most_preferred = self.most_preferred

        grouped = defaultdict(list)

        for learner in self.learners:
            for module_id in most_preferred[learner.id]:
                module = self.modules[module_id]

                if not learner.prefers_over_self_study(module):
                    break

                grouped[learner].append(module)

        return grouped

    @property
    @lru_cache(1)
    def qualifications(self) -> np.ndarray:
        """
        Returns the teacher qualification matrix, as a NumPy array.
        Qualifications are a matrix of teachers (rows) to modules (columns),
        where each element represents the given teacher's qualification for
        the given module. A zero element indicates the teacher is not qualified
        to teach the given module.
        """
        return np.asarray(self._data['qualifications'], dtype=int)

    @property
    @lru_cache(1)
    def learners(self) -> List[Learner]:
        return [Learner(**data) for data in self._data['learners']]

    @property
    @lru_cache(1)
    def teachers(self) -> List[Teacher]:
        return [Teacher(**data) for data in self._data['teachers']]

    @property
    @lru_cache(1)
    def teachers_by_module(self) -> Dict[Module, List[Teacher]]:
        grouped = defaultdict(list)

        by_module = np.argsort(-self.qualifications, axis=1)

        for teacher in self.teachers:
            for module_id in by_module[teacher.id]:
                if self.qualifications[teacher.id, module_id] == 0:
                    break

                grouped[self.modules[module_id]].append(teacher)

        return grouped

    @property
    @lru_cache(1)
    def classrooms(self) -> List[Classroom]:
        return [Classroom(**data) for data in self._data['classrooms']]

    @property
    @lru_cache(1)
    def classrooms_by_module(self) -> Dict[Module, List[Classroom]]:
        grouped = defaultdict(list)

        for module in self.modules:
            for classroom in self.classrooms:
                if classroom.is_qualified_for(module):
                    grouped[module].append(classroom)

        return grouped

    @property
    @lru_cache(1)
    def modules(self) -> List[Module]:
        """
        Returns a list of modules. The last module in the list is the
        self-study module.
        """
        modules = [Module(**data) for data in self._data['modules']]
        modules.append(self.self_study_module)

        return modules

    @property
    @lru_cache(1)
    def self_study_module(self) -> Module:
        return Module(id=SELF_STUDY_MODULE_ID, room_type=999, qualification=3)

    @property
    @lru_cache(1)
    def penalty(self) -> float:
        """
        Returns the self-study penalty.
        """
        return self._data['parameters']['penalty']

    @property
    @lru_cache(1)
    def min_batch(self) -> int:
        return self._data['parameters']['min_batch']

    @property
    @lru_cache(1)
    def max_batch(self) -> int:
        return self._data['parameters']['max_batch']

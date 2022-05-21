from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass, field
from functools import cached_property
from heapq import heapify

import numpy as np
from scipy import sparse

from src.constants import SELF_STUDY_MODULE_ID
from .Classroom import Classroom
from .Learner import Learner
from .Module import Module
from .Teacher import Teacher


@dataclass(frozen=True)
class Problem:
    _data: dict[str, ...] = field(hash=False)

    @classmethod
    def from_file(cls, loc: str) -> Problem:
        """
        Builds a Problem object for the experiment data file at the given
        location.
        """
        with open(loc, "r") as file:
            data = json.load(file)

        p = np.zeros((len(data['learners']), len(data['modules'])))

        for (l, m), pref in data['preferences']:
            p[l, m] = pref

        data = {**data, 'preferences': p}
        return cls(data)

    def to_file(self, loc: str):
        """
        Writes the problem data to the given location.
        """
        with open(loc, "w") as file:
            p = sparse.dok_matrix(self._data['preferences'])
            p = list([tuple(map(int, k)), float(v)] for k, v in p.items())

            data = {**self._data, 'preferences': p}
            json.dump(data, file)

    @cached_property
    def instance(self) -> int:
        return int(self._data['instance'])

    @cached_property
    def num_learners(self) -> int:
        return len(self._data['learners'])

    @cached_property
    def num_courses(self) -> int:
        """
        There are 48 modules per course, excluding the self-study module.
        """
        return (len(self.modules) - 1) // 48

    @cached_property
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
        self_study_pref = self.penalty * np.max(preferences, axis=1)
        return np.concatenate((preferences, self_study_pref[:, None]), 1)

    @cached_property
    def most_preferred(self):
        """
        Returns the most preferred module (index/ID) per learner.
        """
        by_module = np.argsort(-self.preferences[:, :-1], axis=1)

        # Since only one module per course may be preferred, we can safely
        # discard all the others.
        return by_module[:, :self.num_courses]

    @cached_property
    def prefers_over_self_study(self) -> dict[int, list[int]]:
        """
        Returns a dictionary of modules (IDs), per learner (ID), that are
        preferred over the self-study assignment.
        """
        most_preferred = self.most_preferred
        grouped = defaultdict(list)

        for learner in self.learners:
            for module_id in most_preferred[learner.id]:
                module = self.modules[module_id]

                if not learner.prefers_over_self_study(module):
                    break

                grouped[learner.id].append(module)

        return grouped

    @cached_property
    def learners(self) -> list[Learner]:
        return [Learner(**data) for data in self._data['learners']]

    @cached_property
    def teachers(self) -> list[Teacher]:
        return [Teacher(**data) for data in self._data['teachers']]

    @cached_property
    def teachers_by_module(self) -> dict[Module, list[Teacher]]:
        grouped = defaultdict(list)

        for teacher in self.teachers:
            for module_id in range(teacher.frm_module, teacher.to_module):
                grouped[self.modules[module_id]].append(teacher)

        return grouped

    @cached_property
    def classrooms(self) -> list[Classroom]:
        return [Classroom(**data) for data in self._data['classrooms']]

    @cached_property
    def classrooms_by_module(self) -> dict[Module, list[Classroom]]:
        grouped = defaultdict(list)

        for module in self.modules:
            for classroom in self.classrooms:
                if classroom.is_qualified_for(module):
                    grouped[module].append(classroom)

        return grouped

    @cached_property
    def modules(self) -> list[Module]:
        """
        Returns a list of modules. The last module in the list is the
        self-study module.
        """
        modules = [Module(**data) for data in self._data['modules']]
        modules.append(self.self_study_module)

        return modules

    @cached_property
    def self_study_module(self) -> Module:
        return Module(id=SELF_STUDY_MODULE_ID, room_type=999, qualification=3)

    @cached_property
    def penalty(self) -> float:
        """
        Returns the self-study penalty.
        """
        return self._data['penalty']

    @cached_property
    def min_batch(self) -> int:
        return self._data['min_batch']

    @cached_property
    def max_batch(self) -> int:
        return self._data['max_batch']

    def preferences_by_module(
            self,
            learner_ids: list[int]
    ) -> list[tuple[float, int, list[int]]]:
        """
        Computes the aggregate learner preferences by module, for the passed-in
        learners. This list consists only of modules and learners for which the
        minimum batch size is respected.

        The list forms a heap, ordered by aggregate learner preferences (high
        to low). Use ``heapq`` for modification and access.
        """
        learners_by_module = defaultdict(list)

        for learner_id in learner_ids:
            for module_id in self.prefers_over_self_study[learner_id]:
                learners_by_module[module_id].append(learner_id)

            # Histogram (heap) of (preference, module, learner_ids) tuples.
        histogram = [(-self.preferences[learners, mod_id].sum(),
                      mod_id,
                      learners)
                     for mod_id, learners in learners_by_module.items()
                     if len(learners) >= self.min_batch]

        heapify(histogram)
        return histogram

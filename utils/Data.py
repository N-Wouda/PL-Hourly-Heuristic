from functools import lru_cache
from typing import List

import numpy as np
import simplejson as json


# TODO remove; use heuristic.classes.Problem instead

class Data:
    """
    These are the immutable data drawn from the experiment file.
    """

    def __init__(self, data):
        self._data = data

    @classmethod
    def from_instance(cls, experiment: int, instance: int) -> "Data":
        """
        Builds a Data object for the experiment data file associated with the
        given experiment and instance.
        """
        with open(f"experiments/{experiment}/{instance}.json") as file:
            data = json.load(file)

        return cls(data)

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
    def learners(self) -> List:
        return self._data['learners']

    @property
    @lru_cache(1)
    def teachers(self) -> List:
        return self._data['teachers']

    @property
    @lru_cache(1)
    def classrooms(self) -> List:
        return self._data['classrooms']

    @property
    @lru_cache(1)
    def modules(self) -> List:
        """
        Returns a list of modules. The last module in the list is the
        self-study module.
        """
        modules = self._data['modules'].copy()

        modules.append(dict(id=576,  # self-study module
                            room_type=999,
                            qualification=3))

        return modules

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

    @property
    @lru_cache(1)
    def num_courses(self) -> int:
        """
        There are 48 modules per course, excluding the self-study module.
        """
        return (len(self.modules) - 1) // 48

from functools import lru_cache
from typing import List

import numpy as np
import simplejson as json

from .file_location import file_location


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
        with open(file_location(experiment, instance)) as file:
            data = json.load(file)

        return Data(data)

    @property
    @lru_cache(1)
    def preferences(self):
        preferences = np.asarray(self._data["preferences"])

        # Preferences, and the self-study module preference
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
    def qualifications(self):
        return np.asarray(self._data['qualifications'])

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
        modules = self._data['modules'].copy()

        modules.append(dict(id=-1,                  # self-study module
                            room_type=999,
                            qualification=3))

        return modules

    @property
    @lru_cache(1)
    def penalty(self) -> float:
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

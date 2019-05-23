from functools import lru_cache
from typing import List

import numpy as np


class Data:
    """
    These are the immutable data drawn from the experiment file.
    """
    def __init__(self, data):
        self._data = data

    @property
    @lru_cache(1)
    def preferences(self):
        preferences = np.asarray(self._data["preferences"])

        # Preferences, and the self-study module preference
        return np.concatenate((preferences, np.max(preferences, 1)[:, None]), 1)

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

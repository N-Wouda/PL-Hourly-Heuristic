from typing import Generator

import numpy as np

from heuristic.Configuration import Configuration


def accept(new: float, old: float) -> float:
    """
    Computes the acceptance probability according to a simulated annealing
    scheme. <https://en.wikipedia.org/wiki/Simulated_annealing#Pseudocode>.
    """
    temperature = next(_temp)

    if temperature <= 1:
        return 0

    return np.exp((old - new) / temperature)


def _get_temperature() -> Generator[float, None, None]:
    """
    Generator method that returns the current temperature, to be used in
    determining the acceptance probability.
    """
    temperature = Configuration.INITIAL_TEMPERATURE

    while True:
        yield temperature                                           # see p. 9
        temperature = temperature * Configuration.TEMPERATURE_DECAY


_temp = _get_temperature()

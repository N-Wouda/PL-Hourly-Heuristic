import numpy as np
from numpy.random import Generator

from src.classes import Problem
from .learners_to_remove import learners_to_remove


def random_selection(generator: Generator):
    """
    Implements a random selection mechanism, which selects random indices for
    a certain list of num_learners length (e.g., for a cost computation),
    favouring smaller indices.
    """
    problem = Problem()

    triangle = np.arange(learners_to_remove(), 0, -1)

    probabilities = np.ones(problem.num_learners)
    probabilities[:learners_to_remove()] = triangle
    probabilities = probabilities / np.sum(probabilities)

    return generator.choice(problem.num_learners,
                            learners_to_remove(),
                            replace=False,
                            p=probabilities)

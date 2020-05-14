import numpy as np
from alns.criteria import SimulatedAnnealing

# 12 * 48 = 576 regular modules, so the final index/ID for self-study is 576.
SELF_STUDY_MODULE_ID = 576

WEIGHTS = [40, 10, 1, 1]
ITERATIONS = 15000
DECAY = 0.95
DEGREE_OF_DESTRUCTION = 0.2

MAX_WORSE = 0.05
ACCEPTANCE_PROBABILITY = 0.5


def get_criterion(init_objective: float) -> SimulatedAnnealing:
    """
    Returns an SA object with initial temperature such that there is a 50%
    chance of selecting a solution up to 5% worse than the initial solution.
    The step parameter is then chosen such that the temperature reaches 1 in
    the set number of iterations.
    """
    start_temp = MAX_WORSE * init_objective / np.log(ACCEPTANCE_PROBABILITY)
    step = (1 / (start_temp - 1)) ** (1 / ITERATIONS)

    return SimulatedAnnealing(start_temp, 1, step, method="exponential")

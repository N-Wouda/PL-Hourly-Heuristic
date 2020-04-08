import sys

import matplotlib.pyplot as plt
import numpy.random as rnd
from alns import ALNS

from heuristic.classes import Problem
from heuristic.constants import CRITERION, DECAY, ITERATIONS, WEIGHTS
from heuristic.functions import initial_solution
from utils import instances
from .destroy_operators import DESTROY_OPERATORS
from .repair_operators import REPAIR_OPERATORS


def run(experiment: int, instance: int):
    Problem.from_instance(experiment, instance)

    # E.g. for exp 72 and inst. 1, this becomes 7201. This way, even for inst.
    # 100, there will never be overlap between random number streams across
    # experiments.
    alns = ALNS(rnd.RandomState(100 * experiment + instance))

    for operator in DESTROY_OPERATORS:
        alns.add_destroy_operator(operator)

    for operator in REPAIR_OPERATORS:
        alns.add_repair_operator(operator)

    init = initial_solution()
    result = alns.iterate(init, WEIGHTS, DECAY, CRITERION, ITERATIONS)

    result.plot_objectives()
    plt.show()
    #
    # print(result.best_state.objective())
    #
    # write_result(result.best_state, MethodType.HEURISTIC, experiment, instance)


if __name__ == "__main__":
    # The implicit assumption is that the first argument is the experiment
    # number, and the second the instance. This is explained in the readme.
    for inst in instances():
        run(int(sys.argv[1]), int(inst))

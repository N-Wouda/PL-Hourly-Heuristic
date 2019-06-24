import sys

import numpy as np

from utils import Data, instances, MethodType, write_result
from .Configuration import Configuration
from .adaptive_large_neighbourhood_search import \
    adaptive_large_neighbourhood_search
from .diagnostics import diagnostics


def run(experiment: int, instance: int):
    if Configuration.FIX_SEED:
        np.random.seed(19950215)            # TODO generate seeds

    data = Data.from_instance(experiment, instance)

    last, best, history, weights = adaptive_large_neighbourhood_search(data)

    if Configuration.OUTPUT_DIAGNOSTICS:
        diagnostics(last, best, history, weights)

    write_result(best, MethodType.HEURISTIC, experiment, instance)


if __name__ == "__main__":
    # The implicit assumption is that the first argument is the experiment
    # number, and the second the instance. This is explained in the readme.
    for inst in instances():
        run(sys.argv[1], inst)

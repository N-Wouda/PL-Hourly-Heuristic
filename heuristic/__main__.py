import sys

import numpy.random as rnd
from alns import ALNS
from alns.criteria import HillClimbing

from utils import Data, instances, MethodType, write_result
from .initial_solution import initial_solution
from .operators import OPERATORS


def run(experiment: int, instance: int):
    data = Data.from_instance(experiment, instance)

    # E.g. for exp 72 and inst. 1, this becomes 7201. This way, even for inst.
    # 100, there will never be overlap between random number streams across
    # experiments.
    alns = ALNS(rnd.RandomState(100 * experiment + instance))

    # We don't use the destroy operators, as each operator maps from a feasible
    # state to a feasible state.
    alns.add_destroy_operator(lambda state, *args: state)

    for operator in OPERATORS:
        alns.add_repair_operator(operator)

    result = alns.iterate(initial_solution(data),
                          [3, 2, 1, 0.5],
                          0.8,
                          HillClimbing())

    write_result(result.best_state, MethodType.HEURISTIC, experiment, instance)


if __name__ == "__main__":
    # The implicit assumption is that the first argument is the experiment
    # number, and the second the instance. This is explained in the readme.
    for inst in instances():
        run(int(sys.argv[1]), int(inst))

import sys

import numpy.random as rnd
from alns import ALNS

from heuristic.classes import Problem
from heuristic.constants import DECAY, ITERATIONS, WEIGHTS, get_criterion
from heuristic.functions import initial_solution
from .destroy_operators import DESTROY_OPERATORS
from .local_search import reinsert_learner
from .repair_operators import REPAIR_OPERATORS


def main():
    experiment = "tuning" if sys.argv[1] == "tuning" else int(sys.argv[1])
    instance = int(sys.argv[2])

    Problem.from_instance(experiment, instance)

    if experiment == "tuning":
        generator = rnd.default_rng(instance)
    else:
        # E.g. for exp 72 and inst. 1, this becomes 7201. This way, even for
        # inst. 100, there will never be overlap between random number streams
        # across experiments.
        generator = rnd.default_rng(100 * experiment + instance)

    alns = ALNS(generator)  # noqa

    for operator in DESTROY_OPERATORS:
        alns.add_destroy_operator(operator)

    for operator in REPAIR_OPERATORS:
        alns.add_repair_operator(operator)

    alns.on_best(reinsert_learner)

    init = initial_solution()
    criterion = get_criterion(init.objective())
    result = alns.iterate(init, WEIGHTS, DECAY, criterion, ITERATIONS)

    location = f"experiments/{experiment}/{instance}-heuristic.json"
    result.best_state.to_file(location)  # noqa


if __name__ == "__main__":
    main()

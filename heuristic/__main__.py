import argparse

import numpy.random as rnd
from alns import ALNS

from heuristic.classes import Problem
from heuristic.constants import DECAY, ITERATIONS, WEIGHTS, get_criterion
from heuristic.functions import initial_solution
from .destroy_operators import DESTROY_OPERATORS
from .local_search import reinsert_learner
from .repair_operators import REPAIR_OPERATORS


def parse_args():
    parser = argparse.ArgumentParser(prog="heuristic")

    parser.add_argument("experiment", type=str)
    parser.add_argument("instance", type=int)
    parser.add_argument("--exclude", type=str, default=None)

    args = parser.parse_args()
    args.experiment = "tuning" if args.experiment == "tuning" else int(args.experiment)

    return args


def main():
    args = parse_args()

    Problem.from_instance(args.experiment, args.instance)

    if args.experiment == "tuning":
        generator = rnd.default_rng(args.instance)
    else:
        # E.g. for exp 72 and inst. 1, this becomes 7201. This way, even for
        # inst. 100, there will never be overlap between random number streams
        # across experiments.
        generator = rnd.default_rng(100 * args.experiment + args.instance)

    alns = ALNS(generator)  # noqa

    for operator in DESTROY_OPERATORS:
        if args.exclude == operator.__name__:
            continue

        alns.add_destroy_operator(operator)

    for operator in REPAIR_OPERATORS:
        if args.exclude == operator.__name__:
            continue

        alns.add_repair_operator(operator)

    if args.exclude == "reinsert_learner":
        alns.on_best(reinsert_learner)

    init = initial_solution()
    criterion = get_criterion(init.objective())
    result = alns.iterate(init, WEIGHTS, DECAY, criterion, ITERATIONS)

    location = f"experiments/{args.experiment}/{args.instance}-heuristic.json"
    result.best_state.to_file(location)  # noqa


if __name__ == "__main__":
    main()

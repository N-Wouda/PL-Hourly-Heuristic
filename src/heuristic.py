import argparse

import numpy as np
import numpy.random as rnd
from alns import ALNS
from alns.weight_schemes import SimpleWeights

from src.classes import Problem, Result
from src.constants import DECAY, ITERATIONS, WEIGHTS, get_criterion
from src.destroy_operators import DESTROY_OPERATORS
from src.functions import initial_solution, set_problem
from src.local_search import reinsert_learner
from src.repair_operators import REPAIR_OPERATORS


def parse_args():
    parser = argparse.ArgumentParser(prog="heuristic")

    parser.add_argument("experiment", type=str)
    parser.add_argument("instance", type=int)
    parser.add_argument("--exclude", type=str, default=None)

    args = parser.parse_args()
    args.experiment = "tuning" if args.experiment == "tuning" else int(args.experiment)

    return args


def run_alns(experiment, instance, exclude, problem):
    if experiment == "tuning":
        generator = rnd.default_rng(instance)
    else:
        # E.g. for exp 72 and inst. 1, this becomes 7201. This way, even for
        # inst. 100, there will never be overlap between random number streams
        # across experiments.
        generator = rnd.default_rng(100 * experiment + instance)

    alns = ALNS(generator)  # noqa

    for operator in DESTROY_OPERATORS:
        if exclude != operator.__name__:
            alns.add_destroy_operator(operator)

    for operator in REPAIR_OPERATORS:
        if exclude != operator.__name__:
            alns.add_repair_operator(operator)

    if exclude != "reinsert_learner":
        alns.on_best(reinsert_learner)

    init = initial_solution()
    criterion = get_criterion(init.objective())
    weights = SimpleWeights(WEIGHTS,
                            len(alns.destroy_operators),
                            len(alns.repair_operators),
                            DECAY)

    res = alns.iterate(init, weights, criterion, ITERATIONS, problem=problem)
    lbs = -np.minimum.accumulate(res.statistics.objectives[1:])
    ubs = [float("inf")] * ITERATIONS

    return Result(res.best_state.get_assignments(),  # noqa
                  -res.best_state.objective(),
                  res.statistics.runtimes.tolist(),  # noqa
                  lbs.tolist(),
                  ubs)


def main():
    args = parse_args()

    data_loc = f"experiments/{args.experiment}/{args.instance}.json"
    res_loc = f"experiments/{args.experiment}/{args.instance}-heuristic.json"

    problem = Problem.from_file(data_loc)
    set_problem(problem)

    res = run_alns(**vars(args), problem=problem)
    res.to_file(res_loc)

    print(res)


if __name__ == "__main__":
    main()

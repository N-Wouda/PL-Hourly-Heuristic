from typing import Any, Dict

import numpy as np
import numpy.random as rnd
from ConfigSpace import ConfigurationSpace, UniformIntegerHyperparameter
from alns import ALNS
from alns.weights import SimpleWeights
from smac.facade.smac_bb_facade import SMAC4BB
from smac.scenario.scenario import Scenario

from src.classes import Problem, Result
from src.constants import DECAY, STOP, WEIGHTS, get_criterion
from src.destroy_operators import DESTROY_OPERATORS
from src.functions import initial_solution
from src.local_search import reinsert_learner
from src.repair_operators import REPAIR_OPERATORS


def run_alns(instance, problem, settings: Dict[str, Any]) -> Result:
    generator = rnd.default_rng(instance)
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

    res = alns.iterate(init, weights, criterion, STOP, problem=problem)
    lbs = -np.minimum.accumulate(res.statistics.objectives[1:])
    ubs = [float("inf")] * len(lbs)

    return Result(res.best_state.get_assignments(),  # noqa
                  res.statistics.runtimes.tolist(),  # noqa
                  lbs.tolist(),
                  ubs,
                  -res.best_state.objective())


def evaluate(settings: Dict[str, any]) -> float:
    objs = []

    for instance in range(144):
        # TODO: USE MPI HERE | https://mpi4py.readthedocs.io/
        problem = Problem.from_file(f"experiments/tuning/{instance}.json")
        res = run_alns(instance, problem, settings)
        objs.append(res.objective)

    return np.mean(objs)


def main():
    # TODO add tuning parameters
    cs = ConfigurationSpace()
    cs.add_hyperparameter(UniformIntegerHyperparameter("depth", 2, 100))

    # TODO think about what goes into this
    scenario = Scenario({
        "run_obj": "quality",
        "runcount-limit": 10,
        "cs": cs,
    })

    # TODO how to save config?
    smac = SMAC4BB(scenario=scenario, tae_runner=evaluate)
    best_found_config = smac.optimize()
    print(best_found_config)


if __name__ == "__main__":
    main()

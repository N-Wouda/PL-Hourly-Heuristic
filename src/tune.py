from typing import Any, Dict

import numpy as np
import numpy.random as rnd
from ConfigSpace import (ConfigurationSpace, UniformFloatHyperparameter,
                         UniformIntegerHyperparameter)
from alns import ALNS
from alns.weights import SimpleWeights
from smac.facade.smac_bb_facade import SMAC4BB
from smac.scenario.scenario import Scenario

import src.constants
from src.classes import Problem, Result
from src.constants import STOP, get_criterion
from src.destroy_operators import DESTROY_OPERATORS
from src.functions import initial_solution
from src.local_search import reinsert_learner
from src.repair_operators import REPAIR_OPERATORS


def run_alns(instance, problem, settings: Dict[str, Any]) -> Result:
    generator = rnd.default_rng(instance)
    alns = ALNS(generator)  # noqa

    src.constants.DEGREE_OF_DESTRUCTION = settings["dod"]

    for operator in DESTROY_OPERATORS:
        alns.add_destroy_operator(operator)

    for operator in REPAIR_OPERATORS:
        alns.add_repair_operator(operator)

    alns.on_best(reinsert_learner)

    init = initial_solution()
    criterion = get_criterion(init.objective())
    weights = [settings["w" + str(idx + 1)] for idx in range(4)]
    weights = SimpleWeights(weights,
                            len(alns.destroy_operators),
                            len(alns.repair_operators),
                            settings["decay"])

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
    cs = ConfigurationSpace()
    cs.add_hyperparameter(UniformIntegerHyperparameter("w1", 0, 50))
    cs.add_hyperparameter(UniformIntegerHyperparameter("w2", 0, 50))
    cs.add_hyperparameter(UniformIntegerHyperparameter("w3", 0, 50))
    cs.add_hyperparameter(UniformIntegerHyperparameter("w4", 0, 50))
    cs.add_hyperparameter(UniformFloatHyperparameter("decay", 0, 1))
    cs.add_hyperparameter(UniformFloatHyperparameter("dod", 0, .5))

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

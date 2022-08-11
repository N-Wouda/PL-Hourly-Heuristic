import argparse

import numpy.random as rnd
from ConfigSpace import ConfigurationSpace, UniformFloatHyperparameter
from alns import ALNS
from alns.stop import MaxIterations
from alns.weights import SimpleWeights
from smac.facade.smac_hpo_facade import SMAC4HPO
from smac.scenario.scenario import Scenario

import src.constants
from src.classes import Problem
from src.constants import get_criterion
from src.destroy_operators import DESTROY_OPERATORS
from src.functions import initial_solution, set_problem
from src.local_search import reinsert_learner
from src.repair_operators import REPAIR_OPERATORS


def parse_args():
    parser = argparse.ArgumentParser(prog="tune")
    parser.add_argument("--out_dir", default="out/smac")
    parser.add_argument("--time_limit", type=int, default=3600)

    return parser.parse_args()


def run_alns(config, instance, seed):
    problem = Problem.from_file(f"experiments/tuning/{instance}.json")
    set_problem(problem)

    generator = rnd.default_rng(seed)
    alns = ALNS(generator)  # noqa

    src.constants.DEGREE_OF_DESTRUCTION = config["dod"]

    for operator in DESTROY_OPERATORS:
        alns.add_destroy_operator(operator)

    for operator in REPAIR_OPERATORS:
        alns.add_repair_operator(operator)

    alns.on_best(reinsert_learner)

    init = initial_solution()
    stop = MaxIterations(1_000)
    criterion = get_criterion(init.objective(), stop)
    weights = [config["w" + str(idx + 1)] for idx in range(4)]
    weights = SimpleWeights(weights,
                            len(alns.destroy_operators),
                            len(alns.repair_operators),
                            config["decay"])

    res = alns.iterate(init,
                       weights,
                       criterion,
                       stop,
                       problem=problem)

    return res.best_state.objective()


def main():
    args = parse_args()

    cs = ConfigurationSpace()
    cs.add_hyperparameter(UniformFloatHyperparameter("w1", 0, 25))
    cs.add_hyperparameter(UniformFloatHyperparameter("w2", 0, 25))
    cs.add_hyperparameter(UniformFloatHyperparameter("w3", 0, 25))
    cs.add_hyperparameter(UniformFloatHyperparameter("w4", 0, 25))
    cs.add_hyperparameter(UniformFloatHyperparameter("decay", .5, 1))
    cs.add_hyperparameter(UniformFloatHyperparameter("dod", .1, .5))

    scenario = Scenario({
        "run_obj": "quality",
        "wallclock_limit": args.time_limit,
        "cs": cs,
        "deterministic": False,
        "instances": [[str(inst + 1)] for inst in range(144)],
        "shared_model": True,
        "input_psmac_dirs": args.out_dir,
        "output_dir": args.out_dir,
    })

    smac = SMAC4HPO(scenario=scenario, tae_runner=run_alns)

    best_found_config = smac.optimize()
    print(best_found_config)


if __name__ == "__main__":
    main()

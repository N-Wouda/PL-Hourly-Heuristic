from typing import Dict, List

import simplejson as json

from heuristic.classes import Problem
from utils import State
from . import MEASURES


def compute_measures(experiment: int) -> List[Dict[str, float]]:
    """
    Computes all instance performance measures for the given experiment.
    """
    results = []

    for instance in range(1, 101):
        Problem.from_instance(experiment, instance)

        result = {}

        for method in ["ilp", "heuristic"]:
            try:
                state = _get_state(experiment, instance, method)

                method_result = {method + '_' + func.__name__: func(state)
                                 for func in MEASURES}

                result.update(method_result)
            except:
                print(f"Could not compute measures for exp. {experiment}, "
                      f"inst. {instance}, method {method}.")

        results.append(result)

    return results


def _get_state(experiment: int, instance: int, method: str) -> State:
    with open(f"experiments/{experiment}/{instance}-{method}.json") as file:
        assignments = json.load(file)

    return State.from_assignments(assignments)

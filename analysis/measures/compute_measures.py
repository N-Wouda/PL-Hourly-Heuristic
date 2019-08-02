from typing import List, Dict

import simplejson as json

from . import MEASURES
from utils import Data, file_location, MethodType, State


def compute_measures(experiment: int) -> List[Dict[str, float]]:
    """
    Computes all instance performance measures for the given experiment.
    """
    results = []

    for instance in range(1, 101):
        data = Data.from_instance(experiment, instance)

        result = {}

        for method in [MethodType.HEURISTIC, MethodType.ILP]:
            try:
                state = _get_state(data, experiment, instance, method)

                method_result = {
                    method.value + '_' + func.__name__: func(state)
                    for func in MEASURES}

                result.update(method_result)
            except:
                print(f"Could not compute measures for exp. {experiment}, "
                      f"inst. {instance}, method {method.value}.")

        results.append(result)

    return results


def _get_state(data: Data, experiment: int, instance: int,
               method_type: MethodType) -> State:
    """
    Returns the state object for the given experiment instance, associated
    with the given method.
    """
    with open(file_location(experiment, instance, method_type)) as file:
        assignments = json.load(file)

    return State.from_assignments(data, assignments)

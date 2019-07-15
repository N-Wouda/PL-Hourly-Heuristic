from typing import List, Dict

import simplejson as json

from utils import Data, file_location, MethodType, State


def compute_measures(experiment: int) -> List[Dict[str, float]]:
    """
    Computes all instance performance measures for the given experiment.
    """
    results = []

    for instance in range(1, 101):
        data = Data.from_instance(experiment, instance)

        heuristic = _get_state(data, experiment, instance, MethodType.HEURISTIC)
        ilp = _get_state(data, experiment, instance, MethodType.ILP)

        # TODO compute relevant measures
        results.append({})

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

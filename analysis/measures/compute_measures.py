from typing import Dict, List

from heuristic.classes import Problem, Solution
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
                location = f"experiments/{experiment}/{instance}-{method}.json"
                solution = Solution.from_file(location)

                method_result = {method + '_' + func.__name__: func(solution)
                                 for func in MEASURES}

                result.update(method_result)
            except:
                print(f"Could not compute measures for exp. {experiment}, "
                      f"inst. {instance}, method {method}.")

        results.append(result)

    return results

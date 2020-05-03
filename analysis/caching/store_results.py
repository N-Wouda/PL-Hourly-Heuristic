from typing import List, Dict

import simplejson as json


def store_results(experiment: int, results: List[Dict[str, float]]):
    """
    Saves the results for the given experiment to the filesystem.
    """
    with open(f"experiments/{experiment}/stored_measures.json", "w") as file:
        json.dump(results, file)

from typing import List, Dict

import simplejson as json


def store_results(experiment: int, results: List[Dict[str, float]]):
    """
    Saves the results for the given experiment to the filesystem.
    """
    path = "experiments/{0}/stored_measures.json".format(experiment)

    with open(path, "w") as file:
        json.dump(results, file)

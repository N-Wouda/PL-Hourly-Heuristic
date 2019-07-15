from typing import List, Dict

import simplejson as json


def get_cached_results(experiment: int) -> List[Dict[str, float]]:
    path = "experiments/{0}/stored_measures.json".format(experiment)

    with open(path, 'r') as file:
        return json.load(file)

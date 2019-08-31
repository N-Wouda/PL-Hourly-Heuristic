from typing import List, Dict, Optional, Union

import pandas as pd
import simplejson as json

_PATH = "experiments/{0}/stored_measures.json"


def get_cached_results(experiment: Optional[int] = None) \
        -> Union[List[Dict[str, float]], pd.DataFrame]:
    if experiment is not None:
        return _get_one(experiment)

    return _get_all()


def _get_one(experiment: int):
    with open(_PATH.format(experiment), 'r') as file:
        return json.load(file)


def _get_all():
    def get(experiment):
        df = pd.DataFrame(_get_one(experiment))
        df['experiment'] = experiment

        return df

    # TODO: experiment range should probably not be a hardcoded value
    return pd.concat(map(get, range(1, 73)))

import pathlib


def has_cached_results(experiment: int) -> bool:
    path = "experiments/{0}/stored_measures.json".format(experiment)

    return pathlib.Path(path).is_file()

import pathlib


def has_cached_results(experiment: int) -> bool:
    path = f"experiments/{experiment}/stored_measures.json"

    return pathlib.Path(path).is_file()

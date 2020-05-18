import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from heuristic.classes import Problem, Solution
from .measures import MEASURES

pd.set_option('display.max_rows', None)  # display all rows.
pd.set_option('display.float_format', '{:.2f}'.format)  # two decimals.


def parse_args():
    parser = argparse.ArgumentParser(prog="analysis",
                                     description="Analyse experiment results.")

    parser.add_argument("method",
                        help="Solution method to analyse."
                             " One of {ilp, heuristic}.")

    parser.add_argument("experiment", help="Experiment number.")
    parser.add_argument("-f", "--force", action="store_true",
                        help="Force computation; do not use cache.")

    return parser, parser.parse_args()


def compute(parser, args):
    measures = []

    for instance in np.arange(1, 101):
        location = Path(f"experiments/{args.experiment}/"
                        f"{instance}-{args.method}.json")

        if not location.exists():
            print(f"{parser.prog}: {location} does not exist; skipping.")
            continue

        Problem.from_instance(args.experiment, instance)
        solution = Solution.from_file(location)

        measures.append({name: func(solution)
                         for name, func in MEASURES.items()})

    return pd.DataFrame.from_records(measures, columns=MEASURES.keys())


def main():
    parser, args = parse_args()

    cache = Path(f"analysis/cache/{args.experiment}-{args.method}.csv")

    if cache.exists() and not args.force:
        print(f"{parser.prog}: re-using {cache}.")
        data = pd.read_csv(cache)
    else:
        data = compute(parser, args)

    data.set_index("instance", inplace=True)

    print(data, '\n')
    print("Aggregates:", data.aggregate("mean"), sep="\n")

    data.to_csv(cache)


if __name__ == "__main__":
    main()

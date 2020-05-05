import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from heuristic.classes import Problem, Solution

pd.set_option('display.max_rows', None)  # display all rows.
pd.set_option('display.float_format', '{:.2f}'.format)  # two decimals.


def parse_args():
    parser = argparse.ArgumentParser(prog="analysis",
                                     description="Analyse experiment results.")

    parser.add_argument("method",
                        type=str,
                        help="Solution method to analyse."
                             " One of {ilp, heuristic}.")

    parser.add_argument("experiment", type=int, help="experiment number")

    return parser, parser.parse_args()


def main():
    parser, args = parse_args()
    instances = np.arange(1, 101)

    cache = Path(f"analysis/cache/{args.experiment}-{args.method}.csv")

    if cache.exists():
        print(f"{parser.prog}: re-using {cache}.")
        data = pd.read_csv(cache)
    else:
        objectives = []

        for instance in instances:  # gather stats for each instance in exp.
            Problem.from_instance(args.experiment, instance)

            location = Path(f"experiments/{args.experiment}/"
                            f"{instance}-{args.method}.json")

            if not location.exists():
                print(f"{parser.prog}: {location} does not exist; skipping.")
                continue

            solution = Solution.from_file(location)
            objectives.append((instance, -solution.objective()))

        data = pd.DataFrame.from_records(objectives,
                                         columns=("instance", "objective"))

    data.set_index("instance", inplace=True)

    print(data, '\n')
    print("Aggregates:", data.aggregate("mean"), sep="\n")

    data.to_csv(cache)


if __name__ == "__main__":
    main()

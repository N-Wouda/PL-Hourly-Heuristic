import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from src.classes import Problem, Result
from src.functions import set_problem

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
        data_loc = f"experiments/{args.experiment}/{instance}.json"
        problem = Problem.from_file(data_loc)
        set_problem(problem)

        res_loc = Path(f"experiments/{args.experiment}/"
                       f"{instance}-{args.method}.json")

        if not res_loc.exists():
            print(f"{parser.prog}: {res_loc} does not exist; skipping.")
            continue

        res = Result.from_file(res_loc)
        measures.append(dict(instance=instance) | res.measures())

    return pd.DataFrame.from_records(measures)


def main():
    parser, args = parse_args()

    cache = Path(f"cache/{args.experiment}-{args.method}.csv")

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

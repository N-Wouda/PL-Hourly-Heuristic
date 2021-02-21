import argparse
import sys

import simplejson as json

from heuristic.classes import Problem
from .ilp import ilp


def parse_args():
    parser = argparse.ArgumentParser(prog="heuristic")

    parser.add_argument("experiment", type=str)
    parser.add_argument("instance", type=int)

    args = parser.parse_args()
    args.experiment = "tuning" if args.experiment == "tuning" else int(args.experiment)

    return args


def main():
    args = parse_args()

    Problem.from_instance(args.experiment, args.instance)

    result = ilp()
    res_loc = f"experiments/{args.experiment}/{args.instance}-ilp.json"

    with open(res_loc, "w") as file:
        json.dump(result, file)


if __name__ == "__main__":
    main()

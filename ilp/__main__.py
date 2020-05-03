import sys

import simplejson as json

from heuristic.classes import Problem
from .ilp import ilp


def main():
    experiment = int(sys.argv[1])
    instance = int(sys.argv[2])

    Problem.from_instance(experiment, instance)

    result = ilp()

    with open(f"experiments/{experiment}/{instance}-ilp.json", "w") as file:
        json.dump(result, file)


if __name__ == "__main__":
    main()

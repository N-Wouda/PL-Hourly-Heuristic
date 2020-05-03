import sys

import simplejson as json

from heuristic.classes import Problem
from utils import instances
from validator.rules import RULES


def process(experiment: int, instance: int):
    """
    Validates the given experiment instance.
    """
    Problem.from_instance(experiment, instance)

    for method in ["ilp", "heuristic"]:
        path = f"experiments/{experiment}/{instance}-{method}.json"

        try:
            with open(path) as file:
                solution = [tuple(assignment) for assignment in json.load(file)]
        except IOError:
            pass
        else:
            for rule in RULES:
                if not rule(solution):
                    print(f"{path}: solution violates {rule.__name__}.")


def main():
    # The implicit assumption is that the first argument is the experiment
    # number, and the second the instance. This is explained in the readme.
    for inst in instances():
        process(sys.argv[1], inst)


if __name__ == "__main__":
    main()

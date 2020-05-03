import sys

import simplejson as json

from heuristic.classes import Problem
from validator.rules import RULES


def process(experiment: int, instance: int):
    """
    Validates the given experiment instance.
    """
    Problem.from_instance(experiment, instance)

    valid = True

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
                    valid = False
                    print(f"{path}: solution violates {rule.__name__}.")

    return valid


def main():
    if len(sys.argv) < 3:
        instances = list(range(1, 101))
    else:
        instances = [sys.argv[2]]

    exit(0 if all(process(sys.argv[1], inst) for inst in instances) else 1)


if __name__ == "__main__":
    main()

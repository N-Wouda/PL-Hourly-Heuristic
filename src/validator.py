import sys

from src.classes import Problem, Result
from src.rules import RULES


def main():
    experiment = "tuning" if sys.argv[1] == "tuning" else int(sys.argv[1])
    instance = int(sys.argv[2])

    Problem.from_instance(experiment, instance)

    valid = True

    for method in ["ilp", "heuristic"]:
        path = f"experiments/{experiment}/{instance}-{method}.json"

        try:
            result = Result.from_file(path)
        except IOError:
            print(f"{path}: solution file does not exist.")
        else:
            for rule in RULES:
                if not rule(result.assignments):
                    valid = False
                    print(f"{path}: solution violates {rule.__name__}.")

    exit(0 if valid else 1)


if __name__ == "__main__":
    main()

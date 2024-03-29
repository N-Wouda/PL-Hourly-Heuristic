import sys

from src.classes import Problem, Result
from src.rules import RULES


def main():
    experiment = sys.argv[1]
    instance = sys.argv[2]

    data_loc = f"experiments/{experiment}/{instance}.json"
    problem = Problem.from_file(data_loc)

    valid = True

    for method in ["ilp", "heuristic"]:
        path = f"experiments/{experiment}/{instance}-{method}.json"

        try:
            result = Result.from_file(path)
        except FileNotFoundError:
            print(f"{path}: solution file does not exist.")
        else:
            for rule in RULES:
                if not rule(problem, result.assignments):
                    valid = False
                    print(f"{path}: solution violates {rule.__name__}.")

    exit(0 if valid else 1)


if __name__ == "__main__":
    main()

import sys
from pathlib import Path

import numpy as np
import pandas as pd

from heuristic.classes import Problem, Solution

pd.set_option('display.max_rows', None)  # display all rows.


def main():
    experiment = int(sys.argv[1])
    instances = np.arange(1, 101)

    cache = Path(f"analysis/cache/{experiment}.csv")

    if cache.exists():
        print(f"{sys.argv[0]}: re-using {cache}.")
        data = pd.read_csv(cache)
    else:
        objectives = []

        for instance in instances:  # gather stats for each instance in exp.
            Problem.from_instance(experiment, instance)

            location = f"experiments/{experiment}/{instance}-heuristic.json"
            solution = Solution.from_file(location)

            objectives.append(-solution.objective())

        data = pd.DataFrame(objectives, instances, columns=["objective"])

    print(data, '\n')
    print("Aggregates:")
    print(data.aggregate("mean"))

    data.to_csv(f"analysis/cache/{experiment}.csv", index=False)


if __name__ == "__main__":
    main()

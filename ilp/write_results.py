import ast
import sys

import simplejson as json

from .post_process import post_process


def write_results(num_exp, data, solver):
    score = 0

    assignments = post_process(data, solver)

    for assignment in assignments:
        i, j, k, l = ast.literal_eval(assignment)

        score += solver.P[i, j] * assignments[str((i, j, k, l))]

        if j == len(data["modules"]) - 1:  # self-study
            score -= solver.w * assignments[str((i, j, k, l))]

    location = sys.argv[1] + "/{0}-result.json"

    with open(location.format(num_exp), "w") as file:
        json.dump(dict(assignments), file)

    return score

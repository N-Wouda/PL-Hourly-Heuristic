"""
Makes the random instances used in the numerical experiments section of the
paper. See there for details.
"""

import csv
from concurrent.futures import ThreadPoolExecutor
from typing import Any

import numpy as np
from pyDOE2 import fullfact

from src.classes import Problem
from scipy import sparse


def parameter_levels() -> dict[str, Any]:
    learners = [800, 1600, 2400]
    instances = [100]
    penalty = [.5, .75]
    min_batch = [5]
    max_batch = [30]
    progress = [0, 1, 2, 3]
    qualifications = [(1, 0, 0), (0.5, 0.5, 0), (0.4, 0.4, 0.2)]
    split = [True, False]
    courses = [(4, 1), (4, 1), (3, 1), (4, 1), (2, 1), (1, 2), (3, 3), (1, 4),
               (3, 1), (2, 1), (2, 5), (2, 6)]  # (workload, room type) tuples
    modules = [48]

    return locals()


def make_and_write_instances(experiment: int, values: dict[str, Any]):
    """
    A long but mostly straightforward function that makes the experiment
    instances discussed in the paper. This function is legacy code, and has
    mostly been copied verbatim from the bachelor thesis implementation.
    """
    # 1. Create the learner data.
    learners = []
    year = 0

    for idx in range(values['learners']):
        # fairly split the learners into six evenly spaced groups, so each
        # nominal year has the same number of learners.
        if not idx % (values['learners'] // 6 + 1):
            year += 1

        learners.append(dict(id=idx, year=year))

    # 2. Create classroom data.
    classrooms = ...  # TODO

    # 3. Create module data.
    modules = []

    for course, (_, room_type) in enumerate(values['courses']):
        for mod in range(values['modules']):
            is_first = mod >= (values['modules'] // 2)

            modules.append(dict(id=course * values['modules'] + mod,
                                room_type=room_type,
                                qualification=2 - is_first))  # bool as int

    # 4. Create teacher data.
    teachers = [dict(id=idx) for idx in range(len(values['learners']) // 10)]

    # 5. Create teacher qualification matrix.
    qualifications = ...  # TODO

    for instance in range(1, 101):
        # 6. Create the instance-specific learner preferences.
        preferences = np.zeros((len(learners), len(modules)))

        for course, _ in enumerate(values['courses']):
            prefs = np.random.exponential(scale=2, size=(len(learners),))

            for idx, learner in enumerate(learners):
                loc = 8 * (learner['year'] - 1) + 4
                preferences[idx, values['modules'] * course + loc] = prefs[idx]

        # TODO check preference matrix

        # 7. Create instance and write to file.
        instance = Problem(dict(
            experiment=experiment,
            instance=instance,
            preferences=preferences,
            qualifications=qualifications,
            learners=learners,
            classrooms=classrooms,
            modules=modules,
            teachers=teachers,
            penalty=values['penalty'],
            min_batch=values['min_batch'],
            max_batch=values['max_batch'],
        ))

        instance.to_file(f"experiments/{experiment}/{instance}.json")


def main():
    np.random.seed(42)

    levels = parameter_levels()
    num_levels = [len(level) for level in levels.values()]
    experiments = []

    with ThreadPoolExecutor() as executor:
        for num, design in enumerate(fullfact(num_levels), 1):
            exp = {key: value[int(idx)]
                   for (key, value), idx in zip(levels.items(), design)}

            exp["index"] = num

            executor.submit(make_and_write_instances, num, exp)
            experiments.append(exp)

    with open("experiments/experiments.csv", "w", newline='') as fh:
        writer = csv.DictWriter(fh, ["index"] + list(levels.keys()))
        writer.writeheader()
        writer.writerows(experiments)


if __name__ == "__main__":
    main()

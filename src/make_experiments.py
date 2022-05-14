"""
Makes the random instances used in the numerical experiments section of the
paper. See there for details.
"""

import csv
import itertools
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

import numpy as np
from iteround import saferound
from pyDOE2 import fullfact
from scipy.stats import expon, norm

from src.classes import Problem


def parameter_levels() -> dict[str, Any]:
    learners = [800, 1200, 1600]
    instances = [100]
    penalty = [.5, .75]
    min_batch = [5]
    max_batch = [30]
    progress = [0, 1, 2, 3]
    preferences = [2]  # mean value for the exponential distribution
    qualifications = [(1, 0, 0), (0.5, 0.5, 0), (0.4, 0.4, 0.2)]
    split = [True, False]
    courses = [[(4, 1), (4, 1), (3, 1), (4, 1), (2, 1), (1, 2), (3, 3), (1, 4),
                (3, 1), (2, 1), (2, 5), (2, 6)]]  # (workload, room type) tuples
    modules = [48]

    return locals()


def make_and_write_instances(experiment: int, values: dict[str, Any]):
    """
    A long but mostly straightforward function that makes the experiment
    instances discussed in the paper. This function is legacy code, and has
    mostly been copied verbatim from the bachelor thesis implementation.
    """
    exp_dir = Path(f"experiments/{experiment}/")
    exp_dir.mkdir(parents=True, exist_ok=True)

    def round_integers(*,
                       by_idx: bool = False,
                       by_roomtype: bool = False,
                       num_values: int):
        total_workload = sum(workload for workload, _ in values['courses'])
        by_item = defaultdict(lambda: 0)

        for idx, (workload, room_type) in enumerate(values['courses']):
            # Number of values allocated to this course (or room type).
            allotted = (workload / total_workload) * num_values

            if by_idx:
                by_item[idx] += allotted
            elif by_roomtype:
                by_item[room_type] += allotted
            else:
                raise ValueError("Either by_idx or by_roomtype must be set.")

        # see https://stackoverflow.com/a/52807416/4316405
        return dict(zip(by_item.keys(),
                        map(int, saferound(by_item.values(), places=0))))

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
    classrooms = []
    idx = itertools.count(0)

    # - regular classrooms for each room type.
    classrooms_by_room_type = round_integers(
        by_roomtype=True,
        # number of regular classrooms for this many learners.
        num_values=values['learners'] // (10 if values['split'] else 20)
    )

    for room_type, num_classrooms in classrooms_by_room_type.items():
        for classroom in range(num_classrooms):
            classrooms.append(dict(
                id=next(idx),
                capacity=16 if values['split'] else 32,
                self_study_allowed=room_type == 1,
                room_type=room_type
            ))

    # - self-study classrooms.
    learners2numselfstudy = {800: 3, 1200: 4, 1600: 6}
    for _ in range(learners2numselfstudy[values['learners']]):
        classrooms.append(dict(
            id=next(idx),
            capacity=80,
            self_study_allowed=True,
            room_type=999,  # some unused large number
        ))

    # 3. Create module data.
    modules = []

    for course, (_, room_type) in enumerate(values['courses']):
        for mod in range(values['modules']):
            is_first = mod >= (values['modules'] // 2)

            modules.append(dict(id=course * values['modules'] + mod,
                                room_type=room_type,
                                qualification=2 - is_first))  # bool as int

    # 4. Create teacher data, including qualifications.
    teachers = [dict(id=idx) for idx in range(values['learners'] // 10)]

    module = 0
    teacher = 0

    assignment = round_integers(by_idx=True,
                                num_values=values['learners'] // 10)

    for course, num_teachers in assignment.items():
        distribution = [float(num_teachers * values['qualifications'][degree])
                        for degree in range(len(values['qualifications']))]

        teachers_by_qualification = saferound(distribution, places=0)

        for degree, value in enumerate(map(int, teachers_by_qualification), 1):
            for _ in range(value):
                teachers[teacher]['degree'] = degree
                teachers[teacher]['frm_module'] = module
                teachers[teacher]['to_module'] = module + values['modules']

                teacher += 1

        module += values['modules']

    for instance in range(1, values['instances'] + 1):
        # 5. Create the instance-specific learner preferences.
        preferences = np.zeros((len(learners), len(modules)))

        for course, _ in enumerate(values['courses']):
            prefs = expon.rvs(scale=values['preferences'],
                              size=(len(learners),))

            for idx, learner in enumerate(learners):
                midpoint = 8 * (learner['year'] - 1) + 4
                norm_val = norm.rvs(loc=midpoint, scale=values['progress'])
                loc = min(max(int(round(norm_val)), 0), values['modules'] - 1)

                preferences[idx, values['modules'] * course + loc] \
                    = round(prefs[idx], 3)

        # 6. Create instance and write to file.
        problem = Problem(dict(
            experiment=experiment,
            instance=instance,
            preferences=preferences,
            learners=learners,
            classrooms=classrooms,
            modules=modules,
            teachers=teachers,
            penalty=values['penalty'],
            min_batch=values['min_batch'],
            max_batch=values['max_batch'],
        ))

        problem.to_file(exp_dir / f"{instance}.json")  # noqa


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

import argparse
import time
from collections import defaultdict
from typing import List, Tuple

import numpy as np
from gurobipy import GRB, MVar, Model

from src.classes import Problem, Result
from src.constants import SELF_STUDY_MODULE_ID
from src.functions import get_problem, set_problem


def ilp() -> Result:
    """
    Solves the integer linear programming (ILP) formulation of the hourly
    learner preference problem.
    """
    m, x, y = _make_model()

    start_time = time.perf_counter()
    run_times = []
    upper_bounds = []
    incumbent_objs = []

    def callback(model: Model, where: int):
        if where != GRB.Callback.MIPSOL:
            return

        obj = model.cbGet(GRB.Callback.MIPSOL_OBJ)
        bnd = model.cbGet(GRB.Callback.MIPSOL_OBJBND)

        upper_bounds.append(bnd)
        incumbent_objs.append(obj)
        run_times.append((time.perf_counter() - start_time))

    m.modelSense = GRB.MAXIMIZE
    m.optimize(callback)  # type: ignore

    assignments = _to_assignments(x.getAttr('X'), y.getAttr('X'))
    run_times = np.diff(run_times, prepend=run_times[0]).tolist()

    return Result(assignments,
                  m.objVal,
                  run_times,
                  incumbent_objs,
                  upper_bounds)


def _make_model() -> Tuple[Model, MVar, MVar]:
    m = Model()
    problem = get_problem()

    x = m.addMVar((len(problem.modules),
                   len(problem.classrooms),
                   len(problem.teachers)),
                  vtype=GRB.BINARY,
                  name="module_resources")

    y = m.addMVar((len(problem.learners), len(problem.modules)),
                  vtype=GRB.BINARY,
                  obj=problem.preferences,  # noqa
                  ub=problem.preferences > 0,  # preference indicator
                  name="learner_module")

    for learner in range(problem.num_learners):
        m.addConstr(y[learner, :].sum() == 1, "assignment")

    for module in problem.modules:
        res = x[module.id, :, :].sum()

        m.addConstr(y[:, module.id].sum() >= problem.min_batch * res,
                    "min batch")

        if module != SELF_STUDY_MODULE_ID:
            m.addConstr(y[:, module.id].sum() <= problem.max_batch * res,
                        "max batch")

        rhs = [c.capacity * x[module.id, c.id, :].sum()
               for c in problem.classrooms]

        m.addConstr(y[:, module.id].sum() <= sum(rhs), "capacity")

        for classroom in problem.classrooms:
            lhs = x[module.id, classroom.id, :].sum()
            rhs = int(classroom.is_qualified_for(module))

            m.addConstr(lhs <= rhs, "room type")

        for teacher in problem.teachers:
            lhs = x[module.id, :, teacher.id].sum()
            rhs = int(teacher.is_qualified_for(module))

            m.addConstr(lhs <= rhs, "teacher qualification")

    for teacher in problem.teachers:
        m.addConstr(x[:, :, teacher.id].sum() <= 1, "single use teacher")

    for classroom in problem.classrooms:
        m.addConstr(x[:, classroom.id, :].sum() <= 1, "single use classroom")

    return m, x, y


def _to_assignments(x, y) -> List[List[int]]:
    """
    Turns the solver's decision variables into a series of (learner, module,
    classroom, teacher) assignments, which are then stored to the file system.

    TODO this is legacy code, taken from the old State object. It's not the
     prettiest, but it should work.
    """
    problem = get_problem()

    learner_assignments = [module
                           for learner in range(len(problem.learners))
                           for module in range(len(problem.modules))
                           if y[learner, module] > 0]

    classroom_teacher_assignments = {
        (classroom, teacher): module
        for classroom in range(len(problem.classrooms))
        for teacher in range(len(problem.teachers))
        for module in range(len(problem.modules))
        if x[module, classroom, teacher] > 0}

    assignments = []
    counters = defaultdict(lambda: 0)

    for module in range(len(problem.modules)):
        # Select learners and activities belonging to each module, such
        # that we can assign them below.
        learners = [learner for learner in range(len(problem.learners))
                    if learner_assignments[learner] == module]

        activities = [activity for activity, activity_module
                      in classroom_teacher_assignments.items()
                      if module == activity_module]

        # Assign at least min_batch number of learners to each activity.
        # This ensures the minimum constraint is met for all activities.
        for classroom, teacher in activities:
            for _ in range(problem.min_batch):
                if not learners:
                    break

                assignment = (learners.pop(), module, classroom, teacher)
                assignments.append(list(assignment))

                counters[classroom] += 1

        # Next we flood-fill these activities with learners, until none
        # remain to be assigned.
        for classroom, teacher in activities:
            capacity = problem.classrooms[classroom].capacity

            if module != SELF_STUDY_MODULE_ID:
                capacity = min(problem.max_batch, capacity)

            while learners:
                if counters[classroom] == capacity:  # classroom is full
                    break

                assignment = (learners.pop(), module, classroom, teacher)
                assignments.append(list(assignment))

                counters[classroom] += 1

    return assignments


def parse_args():
    parser = argparse.ArgumentParser(prog="ilp")

    parser.add_argument("experiment", type=str)
    parser.add_argument("instance", type=int)

    args = parser.parse_args()
    args.experiment = "tuning" if args.experiment == "tuning" else int(args.experiment)

    return args


def main():
    args = parse_args()

    data_loc = f"{args.experiment}-{args.instance}.json"
    res_loc = f"{args.experiment}-{args.instance}-ilp.json"

    problem = Problem.from_file(data_loc)
    set_problem(problem)

    result = ilp()
    result.to_file(res_loc)

    print(result)


if __name__ == "__main__":
    main()

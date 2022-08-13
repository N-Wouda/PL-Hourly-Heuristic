import argparse
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

    runtimes = []
    upper_bounds = []
    lower_bounds = []

    def callback(model: Model, where: int):
        if where != GRB.Callback.MIP:
            return

        upper_bounds.append(model.cbGet(GRB.Callback.MIP_OBJBND))
        lower_bounds.append(model.cbGet(GRB.Callback.MIP_OBJBST))
        runtimes.append(model.cbGet(GRB.Callback.RUNTIME))

    m.modelSense = GRB.MAXIMIZE
    m.optimize(callback)  # type: ignore

    lower_bounds.append(m.objVal)
    upper_bounds.append(m.objBound)
    runtimes.append(m.runtime)

    assignments = _to_assignments(x.getAttr('X'), y.getAttr('X'))
    runtimes = np.diff(runtimes, prepend=0).tolist()

    return Result(assignments,
                  runtimes,
                  lower_bounds,
                  upper_bounds,
                  m.objVal)


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

        if module.id != SELF_STUDY_MODULE_ID:  # *not* for self-study
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
    """
    problem = get_problem()

    assignments = []
    counters = defaultdict(lambda: 0)

    for module in range(len(problem.modules)):
        # Select learners and activities belonging to each module, such
        # that we can assign them below.
        learners = [learner
                    for learner in range(len(problem.learners))
                    if y[learner, module] > .5]

        activities = [(classroom, teacher)
                      for classroom in range(len(problem.classrooms))
                      for teacher in range(len(problem.teachers))
                      if x[module, classroom, teacher] > .5]

        # Assign at least min_batch number of learners to each activity.
        # This ensures the minimum constraint is met for all activities.
        for classroom, teacher in activities:
            for _ in range(problem.min_batch):
                assignment = (learners.pop(), module, classroom, teacher)
                assignments.append(list(assignment))
                counters[classroom] += 1

        # Next we flood-fill these activities with learners, until none
        # remain to be assigned.
        for classroom, teacher in activities:
            capacity = problem.classrooms[classroom].capacity

            if module != SELF_STUDY_MODULE_ID:
                capacity = min(problem.max_batch, capacity)

            while learners and counters[classroom] < capacity:
                assignment = (learners.pop(), module, classroom, teacher)
                assignments.append(list(assignment))
                counters[classroom] += 1

    assert len(assignments) == problem.num_learners
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

    data_loc = f"experiments/{args.experiment}/{args.instance}.json"
    res_loc = f"experiments/{args.experiment}/{args.instance}-ilp.json"

    problem = Problem.from_file(data_loc)
    set_problem(problem)

    result = ilp()
    result.to_file(res_loc)

    print(result)


if __name__ == "__main__":
    main()

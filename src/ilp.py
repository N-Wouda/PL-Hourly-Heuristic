import argparse
from collections import defaultdict
from typing import List, Tuple

import simplejson as json
from gurobipy import GRB, Model

from src.classes import Problem
from src.constants import SELF_STUDY_MODULE_ID


def ilp() -> List[Tuple]:
    """
    Solves the integer linear programming (ILP) formulation of the hourly
    learner preference problem.
    """
    m = Model()

    problem = Problem()
    x = m.addMVar((len(problem.modules),
                   len(problem.classrooms),
                   len(problem.teachers)),
                  vtype=GRB.BINARY,
                  name="module_resources")

    y = m.addMVar((len(problem.learners), len(problem.modules)),
                  vtype=GRB.BINARY,
                  name="learner_module")

    m.setObjective((problem.preferences * y).sum(), GRB.MAXIMIZE)

    m.addConstr(y <= (problem.preferences > 0), "preference indicator")

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
            rhs = classroom.is_qualified_for(module)

            m.addConstr(lhs <= rhs, "room type")

        for teacher in problem.teachers:
            lhs = x[module.id, :, teacher.id].sum()
            rhs = teacher.is_qualified_for(module)

            m.addConstr(lhs <= rhs, "teacher qualification")

    for teacher in problem.teachers:
        m.addConstr(x[:, :, teacher.id].sum(1) <= 1, "single use teacher")

    for classroom in problem.classrooms:
        m.addConstr(x[:, classroom.id, :].sum() <= 1, "single use classroom")

    status = m.optimize()

    if status != GRB.Status.OPTIMAL:
        # There is not much that can be done in this case, so we raise an
        # error. Logging should pick this up, but it is nearly impossible
        # for this to happen due to the problem structure.
        raise ValueError("Infeasible!")

    return _to_assignments(x.getAttr('X'), y.getAttr('X'))


def _to_assignments(x, y) -> List[Tuple]:
    """
    Turns the solver's decision variables into a series of (learner, module,
    classroom, teacher) assignments, which are then stored to the file system.

    TODO this is legacy code, taken from the old State object. It's not the
     prettiest, but it should work.
    """
    problem = Problem()

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
    parser = argparse.ArgumentParser(prog="heuristic")

    parser.add_argument("experiment", type=str)
    parser.add_argument("instance", type=int)

    args = parser.parse_args()
    args.experiment = "tuning" if args.experiment == "tuning" else int(args.experiment)

    return args


def main():
    args = parse_args()

    Problem.from_instance(args.experiment, args.instance)

    result = ilp()
    res_loc = f"experiments/{args.experiment}/{args.instance}-ilp.json"

    with open(res_loc, "w") as file:
        json.dump(result, file)


if __name__ == "__main__":
    main()

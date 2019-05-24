from collections import defaultdict


def post_process(data, solver):
    assignments = defaultdict(lambda: 0)
    counters = defaultdict(lambda: 0)

    for j in range(len(data["modules"])):  # each module
        learners = [i
                    for i in range(len(data["learners"]))
                    if solver.assignment[i, j].solution_value]

        room_teacher = [(k, l)
                        for k in range(len(data["classrooms"]))
                        for l in range(len(data["teachers"]))
                        if solver.module_resources[j, k, l].solution_value]

        arguments = assignments, counters, room_teacher, learners, j, solver

        _init_assignment(*arguments)
        _assignment(*arguments, data)

    return assignments


def _init_assignment(assignments, counters, room_teacher, learners, j, solver):
    for k, l in room_teacher:
        for _ in range(solver.delta_min):
            if not learners:
                break

            assignments[str((learners.pop(), j, k, l))] = 1
            counters[k] += 1


def _assignment(assignments, counters, room_teacher, learners, j, solver, data):
    for k, l in room_teacher:
        max_cap = min(solver.delta_max, data["classrooms"][k]["capacity"])

        if j == len(data["modules"]) - 1:   # self-study
            max_cap = data["classrooms"][k]["capacity"]

        while learners:
            if counters[k] == max_cap:
                break  # next room, teacher combination

            assignments[str((learners.pop(), j, k, l))] = 1
            counters[k] += 1

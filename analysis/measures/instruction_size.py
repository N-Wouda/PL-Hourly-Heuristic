from heuristic.classes import Solution


def instruction_size(solution: Solution) -> float:
    """
    Computes the average instruction activity size.
    """
    num_learners = num_classrooms = 0

    for activity in solution.activities:
        if activity.is_instruction():
            num_learners += activity.num_learners
            num_classrooms += 1

    if num_learners == 0:
        return 0

    return num_learners / num_classrooms

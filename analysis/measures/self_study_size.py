from heuristic.classes import Solution


def self_study_size(solution: Solution) -> float:
    """
    Computes the average self-study activity size.
    """
    num_learners = num_classrooms = 0

    for activity in solution.activities:
        if activity.is_self_study():
            num_learners += activity.num_learners
            num_classrooms += 1

    if num_learners == 0:
        return 0

    return num_learners / num_classrooms

from heuristic.classes import Solution


def instruction_activity_sizes(solution: Solution):
    return [activity.num_learners for activity in solution.activities
            if activity.is_instruction()]

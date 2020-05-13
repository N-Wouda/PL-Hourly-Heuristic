from heuristic.classes import Solution


def num_instruction(solution: Solution):
    return sum(activity.num_learners for activity in solution.activities
               if activity.is_instruction())

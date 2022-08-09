from collections import defaultdict
from typing import List, Tuple


def learners_to_teachers(problem, solution: List[Tuple]) -> bool:
    """
    Verifies each learner is assigned to *one* teacher.
    """
    learner_teachers = defaultdict(set)

    for learner, *_, teacher in solution:
        learner_teachers[learner].add(teacher)

    return all(len(value) == 1 for value in learner_teachers.values())

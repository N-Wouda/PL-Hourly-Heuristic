from collections import defaultdict
from typing import List, Tuple


def learners_to_classrooms(solution: List[Tuple]) -> bool:
    """
    Verifies each learner is assigned to *one* classroom.
    """
    learner_classrooms = defaultdict(set)

    for assignment in solution:
        learner, _, classroom, _ = assignment
        learner_classrooms[learner].add(classroom)

    return all(len(value) == 1 for value in learner_classrooms.values())

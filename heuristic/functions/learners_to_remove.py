from heuristic.constants import DEGREE_OF_DESTRUCTION


def learners_to_remove(num_learners: int) -> int:
    return int(DEGREE_OF_DESTRUCTION * num_learners)

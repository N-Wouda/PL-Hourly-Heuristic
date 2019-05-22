from heuristic.Configuration import Configuration


def convex_combination(first: float, second: float) -> float:
    return sum([Configuration.OPERATOR_DECAY * first,
                (1 - Configuration.OPERATOR_DECAY) * second])

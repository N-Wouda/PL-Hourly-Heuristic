from alns.accept import SimulatedAnnealing
from alns.stop import MaxIterations

# 12 (# courses) * 48 (# modules per course) = 576 regular modules, so the final
# index/ID for self-study is 576.
SELF_STUDY_MODULE_ID = 576

WEIGHTS = [50, 10, 1, 1]
STOP = MaxIterations(10_000)
DECAY = 0.8
DEGREE_OF_DESTRUCTION = 0.35

MAX_WORSE = 0.05
ACCEPT_PROB = 0.5


def get_criterion(init_obj: float) -> SimulatedAnnealing:
    return SimulatedAnnealing.autofit(-init_obj,
                                      MAX_WORSE,
                                      ACCEPT_PROB,
                                      STOP.max_iterations)

import sys

import numpy as np

from utils import Data, MethodType, write_result
from .Configuration import Configuration
from .adaptive_large_neighbourhood_search import \
    adaptive_large_neighbourhood_search
from .diagnostics import diagnostics

if Configuration.FIX_SEED:
    np.random.seed(19950215)            # TODO generate seeds

data = Data.from_instance(sys.argv[1], sys.argv[2])

last, best, history, weights = adaptive_large_neighbourhood_search(data)

if Configuration.OUTPUT_DIAGNOSTICS:
    diagnostics(last, best, history, weights)

write_result(best, MethodType.HEURISTIC, sys.argv[1], sys.argv[2])

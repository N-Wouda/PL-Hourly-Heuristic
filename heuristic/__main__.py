import sys

import numpy as np
import simplejson as json

from utils import Data, MethodType, Result, write_result
from .Configuration import Configuration
from .adaptive_large_neighbourhood_search import \
    adaptive_large_neighbourhood_search
from .diagnostics import diagnostics

with open(f"experiments/{sys.argv[1]}/{sys.argv[2]}.json") as file:
    data = Data(json.load(file))

if Configuration.FIX_SEED:
    np.random.seed(19950215)

last, best, history, weights = adaptive_large_neighbourhood_search(data)

if Configuration.OUTPUT_DIAGNOSTICS:
    diagnostics(last, best, history, weights)

write_result(Result(best), MethodType.HEURISTIC, sys.argv[1], sys.argv[2])

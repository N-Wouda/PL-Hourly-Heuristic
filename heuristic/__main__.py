import sys

import simplejson as json

from .adaptive_large_neighbourhood_search import \
    adaptive_large_neighbourhood_search
from .Data import Data


with open(f"experiments/{sys.argv[1]}/{sys.argv[2]}.json") as file:
    data = Data(json.load(file))

result, best = adaptive_large_neighbourhood_search(data)

print(result.evaluate())
print(best.evaluate())

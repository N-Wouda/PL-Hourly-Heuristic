import sys

import simplejson as json

from utils import Data, file_location, MethodType
from .validate import validate

data = Data.from_instance(sys.argv[1], sys.argv[2])

for method_type in MethodType:          # ILP, and heuristic
    path = file_location(sys.argv[1], sys.argv[2], method_type)

    try:
        with open(path) as file:
            solution = [tuple(assignment) for assignment in json.load(file)]
    except IOError:
        print(f"No {method_type.value} solution for exp. {sys.argv[1]},"
              f" inst. {sys.argv[2]}.")
    else:
        result = validate(data, solution)

        print(f"Solution ({method_type.value}) satisfies constraints for"
              f" exp. {sys.argv[1]}, inst. {sys.argv[2]}?", result)

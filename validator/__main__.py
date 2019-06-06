import sys

import simplejson as json

from utils import Data, file_location, MethodType
from .validate import validate

data = Data.from_instance(sys.argv[1], sys.argv[2])

for method_type in MethodType:                          # ILP, and heuristic
    path = file_location(sys.argv[1], sys.argv[2], method_type)

    try:
        with open(path) as file:
            solution = [tuple(assignment) for assignment in json.load(file)]
    except IOError:
        print("No {0} solution for exp. {1}, inst. {2}"
              .format(method_type.value, sys.argv[1], sys.argv[2]))
    else:
        result = validate(data, solution)

        print("Solution ({0}) satisfies constraints for exp. {1},"
              " inst. {2}? {3}".format(method_type.value, sys.argv[1],
                                       sys.argv[2], result))

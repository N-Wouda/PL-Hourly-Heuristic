import sys

import simplejson as json

from utils import Data, file_location, instances, MethodType
from .validate import validate


def process(experiment: int, instance: int):
    """
    Validates the given experiment instance.
    """
    data = Data.from_instance(experiment, instance)

    for method_type in MethodType:                      # ILP, and heuristic
        path = file_location(experiment, instance, method_type)

        try:
            with open(path) as file:
                solution = [tuple(assignment) for assignment in json.load(file)]
        except IOError:
            print("No {0} solution for exp. {1}, inst. {2}"
                  .format(method_type.value, experiment, instance))
        else:
            result = validate(data, solution)

            print("Solution ({0}) satisfies constraints for exp. {1},"
                  " inst. {2}? {3}".format(method_type.value, experiment,
                                           instance, result))


if __name__ == "__main__":
    # The implicit assumption is that the first argument is the experiment
    # number, and the second the instance. This is explained in the readme.
    for inst in instances():
        process(sys.argv[1], inst)

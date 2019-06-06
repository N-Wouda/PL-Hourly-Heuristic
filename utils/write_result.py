from .MethodType import MethodType
from .State import State
import simplejson as json
from .file_location import file_location


def write_result(result: State,
                 method_type: MethodType,
                 experiment: int,
                 instance: int):
    """
    Takes a result object and a method type, and writes the output to the
    filesystem in the appropriate location.
    """
    with open(file_location(experiment, instance, method_type), 'w') as file:
        json.dump(result.to_assignments(), file)

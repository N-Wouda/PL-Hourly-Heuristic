from .MethodType import MethodType
from .Result import Result
import simplejson as json
from .file_location import file_location


def write_result(result: Result,
                 method_type: MethodType,
                 experiment: int,
                 instance: int):
    """
    Takes a result object and a method type, and writes the output to the
    filesystem in the appropriate location.
    """
    with open(file_location(experiment, instance, method_type), 'w') as file:
        json.dump(result.assignments, file)

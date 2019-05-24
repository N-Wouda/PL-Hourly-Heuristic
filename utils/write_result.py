from .MethodType import MethodType
from .Result import Result
import simplejson as json


def write_result(result: Result,
                 method_type: MethodType,
                 num_experiment: int,
                 num_instance: int):
    """
    Takes a result object and a method type, and writes the output to the
    filesystem in the appropriate location.
    """
    with open(_file_name(method_type, num_experiment, num_instance), 'w')\
            as file:
        json.dump(result.assignments, file)


def _file_name(method_type: MethodType,
               num_experiment: int,
               num_instance: int) -> str:
    return f"experiments/{num_experiment}/{num_instance}" \
           f"-{method_type.value}.json"

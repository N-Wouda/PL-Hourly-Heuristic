from typing import Optional
from .MethodType import MethodType


def file_location(experiment: int,
                  instance: int,
                  method_type: Optional[MethodType] = None) -> str:
    """
    Returns the file location for the given experiment, instance, and method.
    When method is not passed, the location of the data file (not solution
    instance) is returned.
    """
    if method_type is None:
        return "experiments/{0}/{1}.json".format(experiment, instance)

    return "experiments/{0}/{1}-{2}.json".format(experiment, instance,
                                                 method_type.value)

import sys
from typing import List

# TODO (re)move; not in utils/


def instances() -> List[int]:
    """
    Returns a list of instances based on the passed-in CLI instance option.
    """
    if len(sys.argv) < 3:
        return list(range(1, 101))          # of all experiment instances.
    else:
        return [sys.argv[2]]

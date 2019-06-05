from typing import List, Tuple

from utils import Data
from .constraints import CONSTRAINTS


def validate(data: Data, solution: List[Tuple]) -> bool:
    """
    Checks if the required constraints hold on the passed-in solution.
    """
    return all(constraint(data, solution)
               for constraint in CONSTRAINTS)

from typing import List, Tuple

from utils import Data
from .rules import RULES


def validate(data: Data, solution: List[Tuple]) -> bool:
    """
    Checks if the required validation rules hold on the passed-in solution.
    """
    return all(rule(data, solution) for rule in RULES)

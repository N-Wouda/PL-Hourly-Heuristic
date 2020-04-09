from dataclasses import dataclass


@dataclass(frozen=True)
class Learner:
    id: int
    year: int

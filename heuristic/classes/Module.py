from dataclasses import dataclass

from heuristic.constants import SELF_STUDY_MODULE_ID


@dataclass(order=True, frozen=True)
class Module:
    id: int
    room_type: int
    qualification: int

    def is_self_study(self) -> bool:
        return self.id == SELF_STUDY_MODULE_ID

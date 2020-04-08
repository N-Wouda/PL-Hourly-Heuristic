from dataclasses import dataclass


@dataclass
class Classroom:
    id: int
    room_type: int
    capacity: int
    self_study_allowed: bool

    def is_self_study_allowed(self) -> bool:
        return self.self_study_allowed

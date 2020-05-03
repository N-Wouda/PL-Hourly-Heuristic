from dataclasses import dataclass

from .Module import Module


@dataclass(frozen=True)
class Classroom:
    id: int
    room_type: int
    capacity: int
    self_study_allowed: bool

    def is_self_study_allowed(self) -> bool:
        return self.self_study_allowed

    def is_qualified_for(self, module: Module) -> bool:
        """
        Tests if this classroom is qualified to host an activity for the
        passed-in module. This is done on room type for regular modules, and
        self-study flag for the self-study assignment.
        """
        if module.is_self_study():
            return self.is_self_study_allowed()

        return module.room_type == self.room_type

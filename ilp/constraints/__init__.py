from .LearnerScheduleConflict import LearnerScheduleConflict
from .MaxBatchConstraint import MaxBatchConstraint
from .MinBatchConstraint import MinBatchConstraint
from .RoomTypeConstraint import RoomTypeConstraint
from .SelfStudyAllowedConstraint import SelfStudyAllowedConstraint
from .SingularUseConstraint import SingularUseConstraint
from .StrictlyPostiveAssignmentConstraint import StrictlyPositiveAssignmentConstraint
from .TeachingQualificationConstraint import TeachingQualificationConstraint


constraints = [
    LearnerScheduleConflict,
    SingularUseConstraint,
    MaxBatchConstraint,
    MinBatchConstraint,
    RoomTypeConstraint,
    SelfStudyAllowedConstraint,
    SingularUseConstraint,
    StrictlyPositiveAssignmentConstraint,
    TeachingQualificationConstraint
]

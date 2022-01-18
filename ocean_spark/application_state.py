from enum import Enum


class ApplicationState(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    COMPLETED_WITH_WARNINGS = "COMPLETED_WITH_WARNINGS"
    FAILED = "FAILED"
    KILLED = "KILLED"
    TIMED_OUT = "TIMED_OUT"

    @property
    def is_terminal(self) -> bool:
        return self.value in [
            self.COMPLETED,
            self.COMPLETED_WITH_WARNINGS,
            self.FAILED,
            self.KILLED,
            self.TIMED_OUT,
        ]

    @property
    def is_successful(self) -> bool:
        return self.value in [
            self.COMPLETED,
            self.COMPLETED_WITH_WARNINGS,
        ]

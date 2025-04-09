from dataclasses import dataclass


@dataclass(frozen=True, eq=False)
class ServiceException(Exception):
    @property
    def message(self):
        return "A service exception occurred."

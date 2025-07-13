"""Module defining a protocol for buildable types."""

from typing import Protocol


class Buildable(Protocol):
    """Defines a buildable protocol for objects."""

    def build(self) -> None:
        """Buildable types have to implement build."""
        ...

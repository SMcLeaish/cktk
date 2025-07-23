"""Defines a generic protocol for buildable types.

This module provides the Buildable protocol, which describes
objects that implement a `build()` method returning a constructed
instance of a specific type.
"""

from typing import Protocol, Self


class Buildable[T](Protocol):
    """Protocol for types that implement a build method.

    Implementing types must define a `build()` method that returns
    a fully constructed object of type T.

    Returns:
        T: The built or transformed object.
    """

    def build(self) -> Self:
        """Build and return a constructed object.

        Returns:
            T: The resulting built object.
        """
        ...

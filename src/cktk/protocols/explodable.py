"""Protocol that implements the 'explode_column' transformation.

Defines an interface for types that implement column-exploding
behavior.

Implementing types must define a method to explode a specified column
in a dataframe-like object, returning a new object of the same type.

This allows uniform handling of transformation logic across different
dataframe libraries or backends.

Args:
    df (T): The input dataframe to be transformed.
    column (str): The name of the column to explode.

Returns:
    T: A new instance of the dataframe with the specified column
    exploded.y
"""

from abc import abstractmethod
from typing import Protocol, Self
from cktk.core.types import DataFrameType


class Explodable(Protocol):
    """Defines a protocol for exploding a column in a dataframe."""

    def explode(self) -> Self:
        """Explodable types have to implement explode."""
        ...

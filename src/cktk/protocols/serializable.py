"""Protocol that implements the 'to_dict' transformation.

Serializable objects must have a 'df' DataFrameType property.
"""

from typing import Protocol, Self

from cktk.core.types import DataFrameType


class Serializable(Protocol):
    """Defines a protocol for converting a dataframe to a dict."""

    df: DataFrameType

    def apply_to_dict(self) -> Self:
        """Serializable types have to implement apply_to_dict."""
        ...

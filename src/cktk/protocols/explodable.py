"""Protocol that implements the 'explode_column' transformation.

Explodable type objects must have a 'config' property containing
an explode_columns field and a 'df' DataFrameType property.
"""

from typing import Protocol, Self, runtime_checkable

from cktk.core.types import DataFrameType


@runtime_checkable
class Explodable(Protocol):
    """Defines a protocol for exploding columns in a dataframe."""

    explode_columns: list[str] | None
    df: DataFrameType

    def apply_explode(self) -> Self:
        """Explodable types have to implement explode."""
        ...

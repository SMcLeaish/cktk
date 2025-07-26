"""Protocol that implements the 'explode_column' transformation.

Explodable type objects must have a 'config' property containing
an explode_columns field and a 'df' DataFrameType property.
"""

from typing import Protocol, Self

from cktk.core.types import DataFrameType


class ExplodableConfig(Protocol):
    """Explodable types must have an explode_columns property."""

    @property
    def explode_columns(self) -> list[str]:
        """Return the explode_columns property from the config."""
        ...


class Explodable(Protocol):
    """Defines a protocol for exploding columns in a dataframe."""

    config: ExplodableConfig
    df: DataFrameType

    def explode_columns(self) -> Self:
        """Explodable types have to implement explode."""
        ...

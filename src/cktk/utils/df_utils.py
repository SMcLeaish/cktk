"""Module explodes columns on a pandas or polars dataframe.

Accepts Explodable objects.

Columns defined in the config object as explode_columns
as a list of column names as strings will be exploded, the processed
dataframe will replace the Explodable object df property.
"""

import logging
from enum import Enum

import pandas as pd
import polars as pl

from cktk.core.types import DataFrameType
from cktk.protocols.explodable import Explodable

logger = logging.getLogger(__name__)


def convert_to_polars(df: DataFrameType) -> pl.DataFrame:
    if isinstance(df, pd.DataFrame):
        return pl.from_dataframe(df)
    if isinstance(df, pl.DataFrame):
        return df
    logger.error(
        'Received an object with an invalid type %s',
        type(df).__name__,
    )
    raise TypeError


def explode_on_column(obj: Explodable) -> Explodable:
    """Explodes columns on Explodable object.

    Columns defined in the config object as explode_columns
    as a list of column names as strings will be exploded, the
    processed dataframe will replace the Explodable object df
    property.

    Args:
        obj: Explodable object with df parameter as a pandas
        or polars dataframe.

    Returns:
        Explodable object with df parameter exploded and
        replaced.

    Raises:
        TypeError if obj.df is not a pandas or polars dataframe.
    """
    obj.df = obj.df.explode(obj.explode_columns)
    logger.info(
        'Exploded dataframe columns: %s',
        obj.explode_columns,
    )
    return obj


def concatenate_on_columns(df: pl.DataFrame) -> pl.DataFrame: ...

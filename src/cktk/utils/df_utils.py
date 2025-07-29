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


class DF(Enum):
    """Enum for DataFrameType."""

    PANDAS = 'pandas'
    POLARS = 'polars'


def _check_df_type(func: str, df: DataFrameType) -> tuple[DF, pl.DataFrame]:
    if isinstance(df, pd.DataFrame):
        return (DF.PANDAS, pl.from_dataframe(df))
    if isinstance(df, pl.DataFrame):
        return (DF.POLARS, df)
    logger.error(
        '%s received an object with an invalid type %s',
        func,
        type(df).__name__,
    )
    raise TypeError


def explode_util(obj: Explodable) -> Explodable:
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
    df_type, obj.df = _check_df_type(explode_util.__qualname__, obj.df)

    obj.df = obj.df.explode(obj.config.explode_columns)
    logger.info(
        'Exploded %s dataframe columns: %s',
        df_type,
        obj.config.explode_columns,
    )
    return obj

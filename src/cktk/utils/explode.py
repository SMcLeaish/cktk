"""Module explodes columns on a pandas or polars dataframe.

Accepts Explodable objects.

Columns defined in the config object as explode_columns
as a list of column names as strings will be exploded, the processed
dataframe will replace the Explodable object df property.
"""

import logging

import pandas as pd
import polars as pl

from cktk.protocols.explodable import Explodable

logger = logging.getLogger(__name__)


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
    if isinstance(obj.df, pd.DataFrame) or isinstance(obj.df, pl.DataFrame):
        obj.df = obj.df.explode(obj.config.explode_columns)
        return obj
    logger.error(
        'explode_util received an object with an invalid type %s',
        type(obj.df).__name__,
    )
    raise TypeError

import logging

import polars as pl

from cktk.core.types import EdgeList
from cktk.core.network_graph_transformer import NetworkGraphTransformer

logger = logging.getLogger(__name__)


def explode_on_columns(obj: NetworkGraphTransformer) -> pl.DataFrame:
    explode_df = obj.df
    if obj.explode_columns is not None:
        explode_df = obj.df.explode(obj.explode_columns)
        logger.info(
            'Exploded dataframe columns: %s',
            obj.explode_columns,
        )
        return explode_df
    return obj.df


def edges_from_columns(
    df: pl.DataFrame, edges: EdgeList, edge_attrs: list[str]
) -> pl.DataFrame: ...

import logging

import polars as pl

from cktk.core.network_graph_transformer import NetworkGraphTransformer
from cktk.core.types import EdgeList

logger = logging.getLogger(__name__)


class DataFrameValueError(ValueError):
    def __init__(self, value: str):
        msg = f'{value} must be defined'
        super().__init__(msg)


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
) -> pl.DataFrame:
    working_df = df
    if not edges:
        raise DataFrameValueError('edges')

    edge_dfs: list[pl.DataFrame] = []

    for source_col, target_col in edges:
        if (
            source_col not in working_df.columns
            or target_col not in working_df.columns
        ):
            raise ValueError(
                f'Missing expected column: {source_col} or {target_col}'
            )

        selected_cols = [
            pl.col(source_col).alias('source'),
            pl.col(target_col).alias('target'),
        ]
        for attr in self.config.edge_attrs:
            if attr in self.df.columns:
                selected_cols.append(pl.col(attr))

        temp_edges = self.df.select(selected_cols).with_columns([
            pl.lit(target_col).alias('type')
        ])
        edge_dfs.append(temp_edges)

import logging

import polars as pl

from cktk.core.network_graph_transformer import NetworkGraphTransformer
from cktk.core.types import EdgeAttrDict, EdgeList

logger = logging.getLogger(__name__)


class DataFrameValueError(ValueError):
    def __init__(self, value: str):
        msg = f'{value} must be defined'
        super().__init__(msg)


class DataFrameAttributeError(AttributeError):
    def __init__(self, attribute: str | list[str]):
        msg = f'Expected attribute {attribute} not found'
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
    logger.info('No explode column value, skipping explode function.')
    return obj.df


def edges_from_columns(
    obj: NetworkGraphTransformer, df: pl.DataFrame
) -> EdgeList:
    working_df = df
    if not obj.edges:
        # TODO: Catch exception
        logger.error('Edges value must be present. Exiting.')
        raise DataFrameValueError('edges')
    edges = obj.edges
    edge_attrs = obj.edge_attrs
    edge_dfs: list[pl.DataFrame] = []
    label = obj.edge_label_attr
    edges_list: EdgeList = []
    for source_col, target_col in edges:
        if source_col not in working_df.columns:
            logger.warning(f'Source column {source_col} not found. Skipping.')
            continue
        if target_col not in working_df.columns:
            logger.warning(f'Target column {target_col} not found. Skipping.')
            continue

        selected_cols = [
            pl.col(source_col).alias('source'),
            pl.col(target_col).alias('target'),
        ]
        for attr in edge_attrs:
            if attr in working_df.columns:
                selected_cols.append(pl.col(attr))

        temp_edges = working_df.select(selected_cols).with_columns([
            pl.lit(target_col).alias('type')
        ])
        edge_dfs.append(temp_edges)

    edges_df = pl.concat(edge_dfs)

    for row in edges_df.iter_rows(named=True):
        if label is None:
            label = str(row.get('type', ''))
        attrs: EdgeAttrDict = {'label': label}
        for attr in edge_attrs:
            if attr in row:
                attrs[attr] = row[attr]
        edges_list.append((row['source'], row['target'], attrs))
    return edges_list

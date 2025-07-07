"""Base class for Network Graph Object generating plugins."""

import polars as pl

from cktk.core.types import EdgeAttrDict, EdgeList, NodeList
from cktk.schemas.network_graph_config import NetworkGraphConfig
from cktk.schemas.network_graph_object import NetworkGraphObject


class NetworkGraphFactory:
    def __init__(self, config: NetworkGraphConfig):
        self.config: NetworkGraphConfig = config
        self.df: pl.DataFrame
        self.edges_list: EdgeList = []
        self.nodes_list: NodeList = []
        self.edges_df: pl.DataFrame
        self.nodes_df: pl.DataFrame

    def create(self, df: pl.DataFrame) -> NetworkGraphObject:
        """Build a NetworkGraphObject from the input DataFrame.

        This method orchestrates the transformation by exploding columns,
        generating edges, and creating nodes.

        Args:
            df (pl.DataFrame): The input DataFrame to transform.

        Returns:
            NetworkGraphObject: The resulting graph structure.

        """
        self.df = df
        if self.config.filter_on_column and self.config.filter_value:
            self.df = self.df.filter(
                pl.col(self.config.filter_on_column)
                == self.config.filter_value
            )
        self._explode()
        self._create_edges()
        self._create_nodes()

        return NetworkGraphObject(
            nodes=self.nodes_list,
            edges=self.edges_list,
            source=self.config.source,
            metadata={
                'node_size_variable': self.config.node_size_variable,
                'node_color_variable': self.config.node_color_variable,
                'edge_label_variable': self.config.edge_label_variable,
            },
            metrics=None,
            colormap=None,
        )

    def _create_edges(self) -> None:
        """Generate edges based on EDGES and populate `edges_list`.

        Each tuple in EDGES defines a directed edge from source_col to
        target_col. Attributes from EDGE_ATTRS will be included in the edge metadata.

        Raises:
            ValueError: If any specified source or target column is missing.

        """
        if not self.config.edges:
            raise ValueError('EDGES must be defined in the plugin subclass.')

        edge_dfs: list[pl.DataFrame] = []

        for source_col, target_col in self.config.edges:
            if (
                source_col not in self.df.columns
                or target_col not in self.df.columns
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

        if not edge_dfs:
            self.edges_df = pl.DataFrame()
            return

        self.edges_df = pl.concat(edge_dfs)
        self.edges_df = self.edges_df.filter(
            pl.col('source') != pl.col('target')
        ).drop_nulls()

        for row in self.edges_df.iter_rows(named=True):
            label = row.get(self.config.edge_label_variable)
            if label is None:
                label = str(row.get('type', ''))
            attrs: EdgeAttrDict = {'label': label}
            for attr in self.config.edge_attrs:
                if attr in row:
                    attrs[attr] = row[attr]
            self.edges_list.append((row['source'], row['target'], attrs))

    def _create_nodes(self) -> None:
        """Generate nodes from NODES and append to `nodes_list`.

        Uses each node column and attaches the role (column name) to the node.
        """
        node_set: set[str] = set()
        self.nodes_list.clear()

        for col in self.config.nodes:
            if col not in self.df.columns:
                continue

            subset = self.df.filter(
                pl.col(col).is_not_null() & (pl.col(col) != '')
            )
            for row in subset.iter_rows(named=True):
                node = row[col]
                if node in node_set:
                    continue
                node_set.add(node)

                attrs = {k: row[k] for k in self.config.node_attrs if k in row}
                attrs['type'] = col
                self.nodes_list.append((node, attrs))

    def _explode(self) -> None:
        """Explode delimited string columns into multiple rows."""
        if not self.config.explode_columns:
            return

        for col in self.config.explode_columns:
            if col not in self.df.columns:
                continue

            self.df = self.df.with_columns([
                pl.col(col).str.split(self.config.explode_delimiter)
            ])
            self.df = self.df.explode(col)
            self.df = self.df.with_columns([
                pl.col(col).str.strip_chars().alias(col)
            ])

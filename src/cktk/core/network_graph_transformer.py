"""Module transforms a dataframe into a network graph.

Network graph structure is defined in the NetworkGraphConfig object.
"""

from dataclasses import dataclass

import polars as pl

from cktk.utils.df_utils import (
    edges_from_columns,
    explode_on_columns,
)
from cktk.utils.graph_util import GraphType, get_graph_type


@dataclass(eq=True, frozen=True)
class NetworkGraphTransformer:
    """Transformer class, creates a networkx object from a dataframe.

    Implements Explodable and Graphable Protocols.
    """

    def __init__(self) -> None:
        """Initializes a NetworkGraphTransformer object.

        Args:
            df: DataFrameType object
        """
        self.edges: list[tuple[str, str]]
        self.nodes: list[str]
        self.explode_columns: list[str] | None
        self.explode_delimitter: str
        self.node_attrs: list[str]
        self.edge_attrs: list[str]
        self.color_attr: str
        self.weight_attr: str
        self.edge_label_attr: str
        self.directed: bool
        self.multi: bool

    def apply_explode(self) -> pl.DataFrame:
        return explode_on_columns(self)

    def create_graph(self) -> GraphType:
        """Creates networkx graph from a dataframe."""
        if self.explode_columns is not None:
            working_df = self.apply_explode()
        else:
            working_df = self.df
        g = get_graph_type(self)
        edges_from_columns(working_df, self.edges, self.edge_attrs)

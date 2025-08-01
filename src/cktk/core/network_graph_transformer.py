"""Module transforms a dataframe into a network graph.

Network graph structure is defined in the NetworkGraphConfig object.
"""

from dataclasses import dataclass
from typing import Self

import networkx as nx

from cktk.core.types import DataFrameType
from cktk.protocols import Explodable, Graphable
from cktk.utils.df_utils import convert_to_polars, explode_on_column
from cktk.utils.graph_util import GraphType, get_graph_type


@dataclass(eq=True, frozen=True)
class NetworkGraphTransformer(Explodable, Graphable):
    """Transformer class, creates a networkx object from a dataframe.

    Implements Explodable and Graphable Protocols.
    """

    def __init__(self, df: DataFrameType) -> None:
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
        self.df = convert_to_polars(df)

    def apply_explode(self) -> Self:
        """Explodes columns in config.explode_columns list."""
        explode_on_column(self)
        return self

    def create_graph(self) -> GraphType:
        """Creates networkx graph from a dataframe."""
        if self.explode_columns is not None:
            self.apply_explode()
        g = get_graph_type(self)
        return g

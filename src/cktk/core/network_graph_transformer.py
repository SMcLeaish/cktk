"""Module transforms a dataframe into a network graph.

Network graph structure is defined in the NetworkGraphConfig object.
"""

from dataclasses import dataclass
from typing import Self

from cktk.core.types import DataFrameType
from cktk.protocols.explodable import Explodable
from cktk.protocols.graphable import Graphable
from cktk.utils.df_utils import (
    concatenate_on_columns,
    convert_to_polars,
    explode_on_column,
)
from cktk.utils.graph_util import GraphType, get_graph_type


@dataclass(eq=True, frozen=True)
class NetworkGraphTransformer(Explodable, Graphable):
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

    def create_graph(self, df: DataFrameType) -> GraphType:
        self.df = convert_to_polars(df)
        """Creates networkx graph from a dataframe."""
        if self.explode_columns is not None:
            explode_on_columns(self)
        g = get_graph_type(self)
        concatenate_on_columns(self.df, self.edges, self.edge_attrs)

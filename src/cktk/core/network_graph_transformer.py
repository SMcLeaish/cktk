"""Module transforms a dataframe into a network graph.

Network graph structure is defined in the NetworkGraphConfig object.
"""

from dataclasses import dataclass
import logging

import polars as pl

from cktk.core.types import EdgeList, GraphType
from cktk.utils.df_utils import (
    edges_from_columns,
    explode_on_columns,
)
from cktk.utils.graph_util import get_graph_type

logger = logging.getLogger(__name__)


class TransformerAttributeError(AttributeError):
    def __init__(self, value: str):
        msg = f'{value} must be defined'
        super().__init__(msg)


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
        self.edges: EdgeList
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
        self.df: pl.DataFrame

    def create_graph(self) -> GraphType:
        """Creates networkx graph from a dataframe."""
        working_df = explode_on_columns(self)
        g = get_graph_type(self)
        print(g)
        edges_from_columns(working_df, self.edges, self.edge_attrs)

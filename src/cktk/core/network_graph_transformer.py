"""Module transforms a dataframe into a network graph."""

import logging
from dataclasses import dataclass

import polars as pl

from cktk.core.types import GraphType
from cktk.utils.df_utils import (
    edges_from_columns,
    explode_on_columns,
)
from cktk.utils.graph_util import set_graph_type

logger = logging.getLogger(__name__)


class TransformerAttributeError(AttributeError):
    def __init__(self, value: str):
        msg = f'{value} must be defined'
        super().__init__(msg)


@dataclass(eq=True, frozen=True)
class NetworkGraphTransformer:
    """Transformer to create a networkx graph from a dataframe."""

    def __init__(self) -> None:
        """Initializes a NetworkGraphTransformer object."""
        self.edges: list[str]
        self.nodes: list[str]
        self.explode_columns: list[str] | None
        self.explode_delimitter: str
        self.node_attrs: list[str]
        self.edge_attrs: list[str]
        self.color_attr: str | None
        self.weight_attr: str | None
        self.edge_label_attr: str | None
        self.directed: bool
        self.multi: bool
        self.df: pl.DataFrame

    def create_graph(self) -> GraphType:
        """Creates networkx graph from a dataframe.

        Returns:
            networkx graph from NetworkGraphTransformer template
        """
        explode_df = explode_on_columns(self)
        edges_list = edges_from_columns(self, explode_df)
        g = set_graph_type(self)
        return g

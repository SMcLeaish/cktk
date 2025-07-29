"""Module transforms a dataframe into a network graph.

Network graph structure is defined in the NetworkGraphConfig object.
"""

from typing import Self

import networkx as nx

from cktk.core.types import DataFrameType, GraphType
from cktk.dataclasses.network_graph_config import NetworkGraphConfig
from cktk.protocols import Explodable, Graphable
from cktk.utils.df_utils import explode_util


class NetworkGraphTransformer(Explodable, Graphable):
    """Transformer class, creates a networkx object from a dataframe.

    Implements Explodable and Graphable Protocols.
    """

    def __init__(self, config: NetworkGraphConfig, df: DataFrameType) -> None:
        """Initializes a NetworkGraphTransformer object.

        Args:
            config: NetworkGraphConfig object
            df: DataFrameType object
        """
        self.config = config
        self.df = df

    def apply_explode(self) -> Self:
        """Explodes columns in config.explode_columns list."""
        explode_util(self)
        return self

    def create_graph(self) -> Self:
        """Creates networkx graph from a dataframe."""
        self.graph = nx.from_pandas_edgelist(self.df)
        return self

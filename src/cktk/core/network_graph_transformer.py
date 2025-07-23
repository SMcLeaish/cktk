from typing import Self

import networkx as nx

from cktk.core.types import DataFrameType
from cktk.dataclasses.network_graph_config import NetworkGraphConfig
from cktk.protocols import Explodable, Graphable
from cktk.utils.explode import explode_util


class NetworkGraphTransformer[T](Explodable, Graphable[T]):
    def __init__(self, config: NetworkGraphConfig, df: DataFrameType) -> None:
        self.config = config
        self.df = df
        self.explode().graph()

    def explode(self) -> Self:
        self.df = explode_util(self.df, self.config.explode_columns)
        return self

    def graph(self) -> Self:
        self.g = nx.from_pandas_edgelist(self.df)
        return self

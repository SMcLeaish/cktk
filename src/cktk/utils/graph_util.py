"""Module to create a networkx graph.

Accepts a NetworkGraphTransormer object.
"""

from enum import Enum

import networkx as nx
import polars as pl

from cktk.core.types import GraphType
from cktk.protocols.graphable import Graphable


class GraphEnum(Enum):
    GRAPH = ('Graph',)
    DIGRAPH = ('DiGraph',)
    MULTIGRAPH = ('MultiGraph',)
    MULTIDIGRAPH = 'MultiDiGraph'


def create_graph(obj: Graphable) -> GraphType:
    directed = obj.config.directed
    multi = obj.config.multi
    if not directed and not multi:
        return nx.Graph()
    if directed and not multi:
        return nx.DiGraph()
    if not directed and multi:
        return nx.MultiGraph()
    if directed and multi:
        return nx.MultiGraph()
    raise AttributeError

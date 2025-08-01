"""Module to create a networkx graph.

Accepts a NetworkGraphTransormer object.
"""

import networkx as nx

from cktk.core.types import GraphType
from cktk.protocols.graphable import Graphable

GRAPH_TYPE_MAP: dict[tuple[bool, bool], type[GraphType]] = {
    (False, False): nx.Graph,
    (True, False): nx.DiGraph,
    (False, True): nx.MultiGraph,
    (True, True): nx.MultiDiGraph,
}


class GraphTypeError(TypeError):
    def __init__(self, directed: bool, multi: bool):
        msg = f'Unsupported graph configuration:\
         directed={directed}, multi={multi}'
        super().__init__(msg)


def get_graph_type(obj: Graphable) -> GraphType:
    try:
        return GRAPH_TYPE_MAP[obj.directed, obj.multi]()
    except KeyError as e:
        raise GraphTypeError(obj.directed, obj.multi) from e


def add_edges(obj: Graphable) -> GraphType: ...


def add_nodes(obj: Graphable) -> GraphType: ...


def add_weight(obj: Graphable) -> GraphType: ...

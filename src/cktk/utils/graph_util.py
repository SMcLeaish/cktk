"""Module to create a networkx graph.

Accepts a NetworkGraphTransormer object.
"""

import networkx as nx

from cktk.core.network_graph_transformer import NetworkGraphTransformer
from cktk.core.types import GraphType

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


def get_graph_type(obj: NetworkGraphTransformer) -> GraphType:
    try:
        return GRAPH_TYPE_MAP[obj.directed, obj.multi]()
    except KeyError as e:
        raise GraphTypeError(obj.directed, obj.multi) from e


def add_edges(obj: NetworkGraphTransformer) -> GraphType: ...


def add_nodes(obj: NetworkGraphTransformer) -> GraphType: ...


def add_weight(obj: NetworkGraphTransformer) -> GraphType: ...

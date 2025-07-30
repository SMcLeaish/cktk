"""Module to create a networkx graph.

Accepts a NetworkGraphTransormer object.
"""

from collections.abc import Hashable

import networkx as nx

from cktk.protocols.graphable import Graphable

type GraphType = (
    nx.Graph[Hashable]
    | nx.DiGraph[Hashable]
    | nx.MultiGraph[Hashable]
    | nx.MultiDiGraph[Hashable]
    | None
)

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
        return GRAPH_TYPE_MAP[obj.config.directed, obj.config.multi]()
    except KeyError as e:
        raise GraphTypeError(obj.config.directed, obj.config.multi) from e

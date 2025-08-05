from collections.abc import Hashable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import networkx as nx  # pragma: no cover

type GraphType = (
    nx.Graph[Hashable]
    | nx.DiGraph[Hashable]
    | nx.MultiGraph[Hashable]
    | nx.MultiDiGraph[Hashable]
    | None
)

type NodeAttrDict = dict[str, str | float | None]
type EdgeAttrDict = dict[str, str | float | None]

type NodeTuple = tuple[str, NodeAttrDict]
type EdgeTuple = tuple[str, str, EdgeAttrDict]

type NodeList = list[NodeTuple]
type EdgeList = list[EdgeTuple]

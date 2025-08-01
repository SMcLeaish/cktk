"""Protocol for types that implement graph transformation logic.

This module defines a protocol for converting dataframe-like objects
into NetworkX graphs.
"""

from typing import Protocol, runtime_checkable

from cktk.core.types import GraphType


@runtime_checkable
class Graphable(Protocol):
    """Interface for types that implement the 'graph' transformation.

    Implementing types must provide a method to convert an input
    of type T into a NetworkX Graph | DiGraph | MultiGraph |
    MultiDiGraph.
    """

    directed: bool
    multi: bool
    edges: list[tuple[str, str]]

    def create_graph(self) -> GraphType:
        """Construct a NetworkX graph from the input data.

        Args:
            g (T): A dataframe-like object to convert.

        Returns:
            nx.Graph | nx.DiGraph: A NetworkX graph representation
            of the input data.
        """
        ...

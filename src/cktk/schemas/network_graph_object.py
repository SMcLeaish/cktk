from pydantic import BaseModel, Field
from cktk.core.types import NodeList, EdgeList, Source, MetaData, Metrics, ColorMap


class NetworkGraphObject(BaseModel):
    """A data model for representing a network graph.

    Attributes:
        nodes (NodeList): List of nodes with attributes.
        edges (EdgeList): List of edges with attributes.

    """

    nodes: NodeList = Field(default_factory=list)
    edges: EdgeList = Field(default_factory=list)
    source: Source = Field(default_factory=dict)
    metadata: MetaData = Field(default_factory=dict)
    metrics: Metrics
    colormap: ColorMap

import networkx as nx
from cktk.schemas.network_graph_object import NetworkGraphObject
from cktk.core.types import Metrics, ColorMap
from cktk.core.utils.color import create_distinct_hex_colormap


def build_graph(obj: NetworkGraphObject, max_iter: int = 500) -> nx.MultiDiGraph:
    """Construct the graph.

    Returns:
        nx.Graph: The constructed graph.

    """
    G = nx.MultiDiGraph()
    G.add_nodes_from(obj.nodes)
    G.add_edges_from(obj.edges)
    return G


def calculate_centrality_metrics(G: nx.MultiDiGraph, max_iter: int = 500) -> Metrics:
    metrics: Metrics = {
        # "eigenvector_centrality": nx.eigenvector_centrality(G, max_iter),
        "degree_centrality": nx.degree_centrality(G),
        "betweenness_centrality": nx.betweenness_centrality(G),
    }
    return metrics


def add_metrics_to_nodes(G: nx.MultiDiGraph, metrics: Metrics) -> None:
    for metric_name, score_dict in metrics.items():
        nx.set_node_attributes(G, score_dict, name=metric_name)


def add_colormap_to_graph(
    G: nx.MultiDiGraph, colorvar: str, colormap: ColorMap | None
) -> None:
    """Assign a hex color to each node in the graph using the colormap."""
    if not colormap:
        colormap = create_distinct_hex_colormap(G, colorvar)
    for _, data in G.nodes(data=True):
        group = data.get(colorvar) or ""
        data["color"] = colormap.get(group, "#742727")

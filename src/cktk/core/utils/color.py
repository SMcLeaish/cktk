import distinctipy
import networkx as nx

from cktk.core.types import ColorMap


def create_distinct_hex_colormap(G: nx.Graph, colorvar: str) -> ColorMap:
    """Generate and store a distinct hex color map based on node grouping."""
    unique_groups = sorted({
        data.get(colorvar)
        for _, data in G.nodes(data=True)
        if data.get(colorvar) is not None
    })
    colors = distinctipy.get_colors(len(unique_groups))
    colormap: ColorMap = {
        group: distinctipy.get_hex(color)
        for group, color in zip(unique_groups, colors, strict=False)
    }
    return colormap

from typing import Self
import time
import polars as pl
from cktk.schemas.network_graph_config import NetworkGraphConfig
from cktk.core.network_graph_factory import NetworkGraphFactory
from cktk.core.utils.color import create_distinct_hex_colormap
from cktk.core.utils.graph import (
    build_graph,
    calculate_centrality_metrics,
    add_metrics_to_nodes,
    add_colormap_to_graph,
)
from cktk.core.types import Metrics, ColorMap
from cktk.schemas.network_graph_object import NetworkGraphObject


start = time.perf_counter()


class NetworkGraphBuilder:
    def __init__(self, config: NetworkGraphConfig, df: pl.DataFrame):
        self.factory = NetworkGraphFactory(config)
        self.obj = self.factory.create(df)
        print("create complete", time.perf_counter() - start)
        self.graph = build_graph(self.obj)

        print("build_graph complete", time.perf_counter() - start)
        self.obj.metrics = None
        self.obj.colormap = None

    def add_metrics(self) -> Self:
        self.obj.metrics = calculate_centrality_metrics(self.graph)

        print("calculate_centrality_metrics complete", time.perf_counter() - start)
        add_metrics_to_nodes(self.graph, self.obj.metrics)
        print("add metrics to nodes complete", time.perf_counter() - start)
        return self

    def add_colormap(self) -> Self:
        if self.obj.metadata is None:
            raise AttributeError("NetworkGraphObject is missing metadata")
        colorvar = self.obj.metadata.get("node_color_variable")
        if not colorvar:
            raise AttributeError("Metadata missing 'node_color_variable'")
        self.obj.colormap = create_distinct_hex_colormap(self.graph, colorvar)

        print("create_distinct_hex_colormap complete", time.perf_counter() - start)
        add_colormap_to_graph(self.graph, colorvar, self.obj.colormap)
        print("add_color_map_to_graph complete", time.perf_counter() - start)
        return self

    def build(self) -> Self:
        return self

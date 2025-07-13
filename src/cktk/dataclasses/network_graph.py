"""Module defining a network graph dataclass."""

from dataclasses import dataclass


@dataclass(eq=True, frozen=True)
class NetworkGraph:
    """Class for defining fields to represent a network graph."""

    source_columns: list[str]
    target_columns: list[str]
    explode_columns: list[str]
    node_attrs: list[str]
    edge_attrs: list[str]
    color_attr: str
    weight_sttr: str
    edge_label_attr: str

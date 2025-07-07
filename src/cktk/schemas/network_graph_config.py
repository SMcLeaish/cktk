from dstlib.core.types import Source
from pydantic import BaseModel


class NetworkGraphConfig(BaseModel):
    node_size_variable: str
    explode_columns: list[str]
    explode_delimiter: str = ';'
    filter_on_column: str | None
    filter_value: str | None
    edges: list[tuple[str, str]]
    edge_attrs: list[str] = []
    nodes: list[str]
    node_attrs: list[str] = []
    edge_label_variable: str
    node_color_variable: str
    source: Source

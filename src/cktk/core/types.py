from typing import TypeAlias

NodeAttrDict: TypeAlias = dict[str, str | float | None]
EdgeAttrDict: TypeAlias = dict[str, str | float | None]

NodeTuple: TypeAlias = tuple[str, NodeAttrDict]
EdgeTuple: TypeAlias = tuple[str, str, EdgeAttrDict]

NodeList: TypeAlias = list[NodeTuple]
EdgeList: TypeAlias = list[EdgeTuple]

Metrics: TypeAlias = dict[str, dict[str, float]] | None

ColorMap: TypeAlias = dict[str, str] | None

Source: TypeAlias = dict[str, str] | None

MetaData: TypeAlias = dict[str, str] | None

from collections.abc import Hashable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import networkx as nx  # pragma: no cover
    import pandas as pd  # pragma: no cover
    import polars as pl  # pragma: no cover

type DataFrameType = pd.DataFrame | pl.DataFrame | pl.LazyFrame

from unittest.mock import MagicMock

import pytest

from cktk.core.network_graph_transformer import NetworkGraphTransformer


def test_instatiate_network_graph_transformer():
    df = MagicMock()
    config = MagicMock()
    transformer = NetworkGraphTransformer(config, df)
    assert isinstance(transformer, NetworkGraphTransformer)

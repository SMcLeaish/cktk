import yaml
from pathlib import Path
from cktk.schemas.network_graph_config import NetworkGraphConfig


def load_config_from_yaml(path: str | Path) -> NetworkGraphConfig:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"YAML config file not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    return NetworkGraphConfig(**raw)

from cktk.core.types import DataFrameType


def explode_util(df: DataFrameType, columns: str | list[str]) -> DataFrameType:
    return df.explode(columns)

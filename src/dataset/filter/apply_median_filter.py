import pandas as pd


def apply_median_filter(
    df: pd.DataFrame, column: str, window_size: int
) -> pd.DataFrame:
    """_summary_

    Args:
        df (pd.DataFrame): _description_
        column (str): _description_
        window_size (int): _description_

    Returns:
        pd.DataFrame: _description_
    """
    # check if column exist
    if column not in df.columns:
        raise Exception(f"Column ({column}) not found")
    df[column + "_median_filter_" + str(window_size)] = (
        df[column].rolling(window_size).median()
    )
    return df


def acc_filter(
    df: pd.DataFrame, axis: str, window_size: int, threshold: float
) -> pd.DataFrame:
    df = df[
        (
            df["rotated_acceleration_" + axis + "_median_filter_" + str(window_size)]
            > threshold
        )
        | (
            df["rotated_acceleration_" + axis + "_median_filter_" + str(window_size)]
            < -threshold
        )
    ]
    return df

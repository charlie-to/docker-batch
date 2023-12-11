import os
from pprint import pprint

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import scienceplots  # noqa
from shapely import wkt

plt.style.use(["science", "ieee", "japanese"])

DATA_IMPORT_PATH = os.environ.get("DATA_IMPORT_PATH")
PARTICIPANT_NAMES = os.environ.get("PARTICIPANT_NAMES").split(" ")


def add_median_filter(df: pd.DataFrame, col: str, window_size: int) -> pd.DataFrame:
    """
    Add a median filter column to a dataframe.
    :param df: dataframe
    :param col: column name
    :param window_size: window size
    :return: dataframe with new column
    """
    # check if column exists
    if col not in df.columns:
        raise ValueError(f"Column {col} not in dataframe.")
    # add median filter column
    df[col + "_median_filter_" + str(window_size)] = (
        df[col].rolling(window_size).median()
    )
    return df


def filter_cutting_x_axis(df: pd.DataFrame, col: str, threshold: float) -> pd.DataFrame:
    df = df[(df[col] > threshold) | (df[col] < -threshold)]
    return df


def fillter(participant_name: str):
    # Read in the data
    df = pd.read_csv(DATA_IMPORT_PATH + participant_name + "/processed/evt_all.csv")
    columns_name = df.columns.values.tolist()
    columns_name[0] = "time"
    df.columns = columns_name
    df["time"] = pd.to_datetime(df.time, format="ISO8601")
    df["geometry"] = df["geometry"].apply(wkt.loads)
    df = gpd.GeoDataFrame(df, geometry="geometry")
    df.info()

    col_name = "rotated_acceleration_x"
    window_size = [5, 8, 10, 15, 20, 25]
    for ws in window_size:
        df2 = add_median_filter(df, col_name, window_size=ws)
        df2.info()
    pprint(df2)

    df2 = filter_cutting_x_axis(df2, col_name, threshold=0.2)
    pprint(df2.info())
    print("file counts : ", len(df.file_name.unique()))
    print("filtered file name :", str(len(df2["file_name"].unique().tolist())))


if __name__ == "__main__":
    for participant_name in PARTICIPANT_NAMES:
        fillter(participant_name)

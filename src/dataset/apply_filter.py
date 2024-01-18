import os

import geopandas as gpd
import numpy as np
from file_io import read_evt_file
from filter import acc_filter, apply_median_filter

DATA_IMPORT_PATH = os.environ["DATA_IMPORT_PATH"]
PARTICIPANT_NAMES = os.environ["PARTICIPANT_NAMES"].split(" ")


def export_filtered_evt(participant_name: str) -> None:
    # Load the data
    df: gpd.GeoDataFrame = read_evt_file(participant_name=participant_name)
    # apply filter
    df = apply_median_filter(df, column="rotated_acceleration_x", window_size=20)
    df = acc_filter(df, axis="x", window_size=20, threshold=0.2)

    # Export the data
    df.to_csv(
        f"{DATA_IMPORT_PATH}/{participant_name}/processed/filtered_evt.csv", index=False
    )
    # Export file name only
    file_names: np.ndarray = df["file_name"].unique()
    file_names.sort()
    file_names.tofile(
        f"{DATA_IMPORT_PATH}/{participant_name}/processed/filtered_evt_file_name.csv",
        sep="\n",
        format="%s",
    )


if __name__ == "__main__":
    for participant_name in PARTICIPANT_NAMES:
        export_filtered_evt(participant_name=participant_name)

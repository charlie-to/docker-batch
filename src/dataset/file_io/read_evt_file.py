# Read in the data
import os

import geopandas as gpd
import pandas as pd
from shapely import wkt

DATA_IMPORT_PATH = os.environ.get("DATA_IMPORT_PATH")


def read_evt_file(participant_name: str) -> gpd.GeoDataFrame:
    df = pd.read_csv(DATA_IMPORT_PATH + participant_name + "/processed/EVT_ALL.csv")
    columns_name = df.columns.values.tolist()
    columns_name[0] = "time"
    df.columns = columns_name
    df["time"] = pd.to_datetime(df.time, format="ISO8601")
    df["geometry"] = df["geometry"].apply(wkt.loads)
    df = gpd.GeoDataFrame(df, geometry="geometry")
    print("**********")
    df.info()
    return df

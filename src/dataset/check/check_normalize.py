import os

import contextily as cx
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import scienceplots  # import: ignore
from shapely import wkt

plt.style.use(["science", "ieee", "japanese"])

DATA_IMPORT_PATH = os.environ.get("DATA_IMPORT_PATH")


def check_normalize() -> None:
    """check_normalize

    Args:
        df (pd.DataFrame): [description]
        column (str): [description]
    """
    # Read in the data
    df = pd.read_csv(DATA_IMPORT_PATH + "raw/processed/evt_all.csv")
    columns_name = df.columns.values.tolist()
    columns_name[0] = "time"
    df.columns = columns_name
    df["time"] = pd.to_datetime(df.time, format="ISO8601")
    df["geometry"] = df["geometry"].apply(wkt.loads)
    df = gpd.GeoDataFrame(df, geometry="geometry")
    df.info()
    print("file counts : ", len(df.file_name.unique()))

    # Plot the data
    df1 = df.dropna()
    fig, ax = plt.subplots()
    df1.acceleration_x.hist(ax=ax, bins=100)
    fig.savefig(DATA_IMPORT_PATH + "raw/processed/acceleration_x_hist.png")
    plt.close()
    fig, ax = plt.subplots()
    df1.rotated_acceleration_x.hist(ax=ax, bins=100)
    fig.savefig(DATA_IMPORT_PATH + "raw/processed/rotated_acceleration_x_hist.png")
    plt.close()
    # compare the two columns
    fig, ax = plt.subplots()
    ax.hist(df1.acceleration_x, bins=100, alpha=0.8, label="元データ")
    ax.hist(df1.rotated_acceleration_x, bins=100, alpha=0.8, label="回転後データ")
    ax.legend()
    fig.savefig(DATA_IMPORT_PATH + "raw/processed/compare_acceleration_x_hist.png")
    plt.close()

    fig, ax = plt.subplots(figsize=(30, 30))
    df1 = df1.set_crs(epsg=4326, allow_override=True)
    df1 = df1.to_crs(epsg=3857)
    df1.plot(ax=ax, linewidth=5, color="black", alpha=0.2, markersize=3)
    cx.add_basemap(ax=ax, source=cx.providers.OpenStreetMap.Mapnik)
    ax.set_axis_off()
    fig.savefig(DATA_IMPORT_PATH + "raw/processed/evt_all.png", dpi=300)

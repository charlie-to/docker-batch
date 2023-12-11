import os

import contextily as cx
import geopandas as gpd
import matplotlib as mpl
import matplotlib.pyplot as plt
import scienceplots  # noqa: F401

mpl.use("pgf")

plt.style.use(["science", "ieee"])
plt.rcParams["text.usetex"] = True
plt.rcParams["pgf.texsystem"] = "lualatex"
plt.rcParams["font.family"] = "Noto Sans CJK JP"
plt.rcParams["font.serif"] = "Noto Sans CJK JP"
plt.rcParams["pgf.rcfonts"] = False

DATA_IMPORT_PATH: str = os.environ.get("DATA_IMPORT_PATH")
PARTICIPANT_NAMES: list[str] = os.environ.get("PARTICIPANT_NAMES").split(" ")


def check_normalize(df: gpd.GeoDataFrame, participant_name: str) -> None:
    """check_normalize

    Args:
        df (pd.DataFrame): [description]
        column (str): [description]
    """

    # Plot the data
    df1 = df.dropna()
    fig, ax = plt.subplots()
    df1.acceleration_x.hist(ax=ax, bins=100)
    fig.savefig(
        DATA_IMPORT_PATH + participant_name + "/processed/acceleration_x_hist.png"
    )
    plt.close()
    fig, ax = plt.subplots()
    df1.rotated_acceleration_x.hist(ax=ax, bins=100)
    fig.savefig(
        DATA_IMPORT_PATH
        + participant_name
        + "/processed/rotated_acceleration_x_hist.png"
    )
    plt.close()
    # compare the two columns
    fig, ax = plt.subplots()
    ax.hist(df1.acceleration_x, bins=100, alpha=0.8, label="元データ")
    ax.hist(df1.rotated_acceleration_x, bins=100, alpha=0.8, label="座標回転後")
    ax.legend()
    fig.savefig(
        DATA_IMPORT_PATH
        + participant_name
        + "/processed/compare_acceleration_x_hist.png"
    )
    plt.close()

    # fig, ax = plt.subplots(figsize=(20, 20))
    # df1 = df1.set_crs(epsg=4326, allow_override=True)
    # df1 = df1.to_crs(epsg=3857)
    # df1.plot(ax=ax, linewidth=5, color="black", alpha=0.2, markersize=3)
    # cx.add_basemap(ax=ax, source=cx.providers.OpenStreetMap.Mapnik)
    # ax.set_axis_off()
    # fig.savefig(DATA_IMPORT_PATH + participant_name + "/processed/evt_all.png", dpi=300)

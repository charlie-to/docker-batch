import os

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


def plot_hist_raw_rotated(
    df_raw: gpd.GeoDataFrame, df_ans: gpd.GeoDataFrame, participant_name: str
) -> None:
    # make brake files only
    df_raw = df_raw.dropna()
    brake_file_name = df_ans[
        (df_ans.acc_minus == 1) | (df_ans.acc_minus_danger == 1)
    ].file_name.unique()
    brake_file_name = brake_file_name + ".srt"
    df_brake = df_raw[df_raw.file_name.isin(brake_file_name)]
    # Plot the data
    fig, ax = plt.subplots()
    ax.hist(
        df_raw.acceleration_x * 16 / 2048,
        bins=100,
        density=True,
        alpha=0.5,
        label="全データ",
        histtype="bar",
    )
    ax.hist(
        df_brake.acceleration_x * 16 / 2048,
        bins=100,
        density=True,
        alpha=0.5,
        label="減速挙動",
        histtype="bar",
    )
    ax.set_xlabel("ログ値加速度 [G]")
    ax.set_ylabel("度数（規格化後）")
    ax.set_xlim(-1.2, 0)
    ax.legend()
    fig.savefig(
        DATA_IMPORT_PATH + participant_name + "/processed/compare_raw_vs_rotated.png"
    )

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
        df_raw.rotated_acceleration_x,
        bins=100,
        density=True,
        alpha=0.5,
        label="元データ",
    )

    ax.hist(
        df_raw.rotated_acceleration_x.rolling(10).mean(),
        bins=100,
        density=True,
        alpha=0.5,
        label="移動平均フィルタ",
    )

    ax.hist(
        df_raw.rotated_acceleration_x.rolling(20).median(),
        bins=100,
        density=True,
        alpha=0.5,
        label="メディアンフィルタ",
    )
    ax.set_xlabel("加速度 [G]")
    ax.set_ylabel("度数")
    ax.set_xlim(-0.6, 0.6)
    ax.legend()
    fig.savefig(
        DATA_IMPORT_PATH + participant_name + "/processed/compare_raw_vs_filters.png"
    )

    # plot histgram of brake rotated acceleration vs raw acceleration
    fig, ax = plt.subplots()

    ax.hist(
        df_raw.rotated_acceleration_x.rolling(10).mean(),
        bins=100,
        density=True,
        alpha=0.5,
        label="元データ（移動平均フィルタ）",
    )

    ax.hist(
        df_brake.rotated_acceleration_x.rolling(10).mean(),
        bins=100,
        density=True,
        alpha=0.5,
        label="減速挙動（移動平均フィルタ）",
    )
    ax.set_xlabel("加速度 [G]")
    ax.set_ylabel("度数")
    ax.set_xlim(-0.6, 0.6)
    ax.legend()
    fig.savefig(
        DATA_IMPORT_PATH + participant_name + "/processed/compare_raw_vs_brake.png"
    )

    ax.set_xlim(-0.4, -0.2)
    fig.savefig(
        DATA_IMPORT_PATH + participant_name + "/processed/compare_raw_vs_brake_zoom.png"
    )

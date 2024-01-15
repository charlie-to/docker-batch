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


def plot_hist_raw_accuracy(
    df_raw: gpd.GeoDataFrame, df_ans: gpd.GeoDataFrame, participant_name: str
) -> None:
    # make brake files only
    df_raw = df_raw.dropna()
    brake_file_name = df_ans[
        (df_ans.acc_minus == 1) | (df_ans.acc_minus_danger == 1)
    ].file_name.unique()
    brake_file_name = brake_file_name + ".srt"
    df_brake = df_raw[df_raw.file_name.isin(brake_file_name)]

    counts_files = []  # count the number of files by each threshold of acceleration
    thresholds = [num * 0.1 for num in range(-10, 0, 1)]
    # filtered files by each threshold of acceleration
    for threshold in thresholds:
        df_filtered = df_brake[df_brake.acceleration_x < threshold]
        counts_files.append(len(df_filtered.file_name.unique()))

    # Plot counts of files by each threshold of acceleration
    fig, ax = plt.subplots()
    ax.plot(thresholds, counts_files, label="減速挙動")
    ax.set_xlabel("ログ値加速度閾値 [G]")
    ax.set_ylabel("ファイル数")
    fig.savefig(
        DATA_IMPORT_PATH + participant_name + "/processed/compare_raw_vs_threshold.png"
    )

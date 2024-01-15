import os

import matplotlib.pyplot as plt
import pandas as pd
import scienceplots  # noqa: F401
from file_io import read_evt_file

plt.style.use(["science", "ieee"])
DATA_IMPORT_PATH = os.environ["DATA_IMPORT_PATH"]
PARTICIPANT_NAMES = os.environ["PARTICIPANT_NAMES"].split(" ")


def plot_evt_df_acc(df: pd.DataFrame, participant_name: str, file_name: str) -> None:
    fig, ax = plt.subplots()
    df["rotated_acceleration_x"].plot(ax=ax, label="acc_x")
    df["rotated_acceleration_x"].rolling(20).median().plot(ax=ax, label="acc_x_median")
    ax.set_ylim([-0.8, 0.5])
    ax.legend()
    ax.set_xlabel("加速度[G]")
    fig.savefig(
        f"{DATA_IMPORT_PATH}{participant_name}/plot/evt_acc/{file_name}_acc_x.png"
    )
    plt.close()


if __name__ == "__main__":
    for participant_name in PARTICIPANT_NAMES:
        df = read_evt_file(participant_name)
        for file_name in df.file_name.unique().tolist():
            df_file = df[df["file_name"] == file_name]
            plot_evt_df_acc(df_file, participant_name, file_name.split(".")[0])

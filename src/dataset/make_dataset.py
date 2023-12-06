import os

import pandas as pd
from raw.get_acc_all import get_acc_all

data_path: str = os.environ["DATA_IMPORT_PATH"]


def save_evt_all() -> None:
    df1: pd.DataFrame = get_acc_all("EVT")
    df1.to_csv(data_path + "processed/EVT_ALL.csv")
    print("EVT_ALL.csv saved")


def save_rec_all() -> None:
    df2: pd.DataFrame = get_acc_all("REC")
    df2.to_csv("./data/processed/REC_ALL.csv")
    print("REC_ALL.csv saved")


if __name__ == "__main__":
    save_evt_all()
